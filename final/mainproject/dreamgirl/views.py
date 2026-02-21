from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Candidate, Voter, PreApprovedVoter
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import datetime, date, time
import re
import json

# QR Imports
import qrcode
from io import BytesIO
import base64



from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import HRFlowable
from reportlab.lib.enums import TA_CENTER



from .models import ElectionSettings


def download_receipt(request):

    voter_id = request.session.get('voter_id')
    if not voter_id:
        return redirect('login')

    voter = Voter.objects.get(id=voter_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="D-Vote_Official_Receipt.pdf"'

    doc = SimpleDocTemplate(response)
    elements = []

    styles = getSampleStyleSheet()

    # ====== OFFICIAL TITLE ======
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )

    elements.append(Paragraph("D-VOTE OFFICIAL VOTING RECEIPT", title_style))
    elements.append(Spacer(1, 20))

    elements.append(HRFlowable(width="100%", thickness=2, color=colors.black))
    elements.append(Spacer(1, 20))

    # ====== RECEIPT TABLE DATA ======
    voting_date = voter.voted_at.strftime("%d %B %Y") if voter.voted_at else "N/A"
    data = [
       
        ["Voter ID", voter.voter_id],
        ["Aadhaar Number", voter.aadhaar_number],
        ["Constituency", voter.location],
        ["Voting Date ", voting_date],   # 🔥 Added this
        ["Status", "Vote Successfully Cast"]
    ]

    table = Table(data, colWidths=[2.5 * inch, 3 * inch])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    # ====== FOOTER NOTE ======
    footer = Paragraph(
        "This is a system-generated official confirmation receipt. "
        "The vote has been securely recorded in the D-Vote system.",
        styles['Normal']
    )

    elements.append(footer)

    doc.build(elements)

    return response

# ====================================================
# 🕒 COMMON TIME SETTINGS
# ====================================================





def get_time():
    settings = ElectionSettings.objects.first()

    if not settings:
        return None, None, None

    start = timezone.make_aware(
        datetime.combine(settings.voting_date, settings.start_time)
    )

    end = timezone.make_aware(
        datetime.combine(settings.voting_date, settings.end_time)
    )

    now = timezone.localtime(timezone.now())

    return start, end, now


# ====================================================
# 🏠 HOME (Always Allowed)
# ====================================================

def home(request):

    # 🔗 Change IP according to your system
   # result_url = "http://192.168.0.195:8000/final-results/Doranahalli/"

    #qr = qrcode.make(result_url)
    #buffer = BytesIO()
   # qr.save(buffer, format="PNG")
    #qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return render(request, 'dreamgirl/home.html', {
        #"qr_code": qr_base64
    })


# ====================================================
# 📝 REGISTER (Blocked After 6PM)
# ====================================================

def register(request):

    start, end, now = get_time()

    if now > end:
        return redirect('home')

    message = ""

    if request.method == 'POST':
        aadhaar = request.POST.get('aadhaar')
        voter_id = request.POST.get('voter_id')
        email = request.POST.get('email')
        age = int(request.POST.get('age'))
        gender = request.POST.get('gender')   # ✅ ADDED
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if age < 18:
            message = "You must be at least 18 years old."
        elif not re.fullmatch(r"[A-Z]{3}[0-9]{7}", voter_id):
            message = "Invalid Voter ID format."
        elif password != confirm_password:
            message = "Passwords do not match."
        elif not PreApprovedVoter.objects.filter(
                aadhaar_number=aadhaar,
                voter_id=voter_id,
               location__iexact=location).exists():
            message = "You are not eligible."
        elif Voter.objects.filter(voter_id=voter_id).exists():
            message = "Already registered."
        else:
            Voter.objects.create(
                aadhaar_number=aadhaar,
                voter_id=voter_id,
                email=email,
                location=location,
                age=age,           # ✅ ADDED
                gender=gender      # ✅ ADDED
            )

            User.objects.create_user(username=voter_id, password=password)
            return redirect('login')

    return render(request, 'dreamgirl/register.html', {'message': message})


# ====================================================
# 🔐 LOGIN (Blocked After 6PM)
# ====================================================

def login_view(request):

    start, end, now = get_time()

    if now > end:
        return redirect('home')

    if request.method == "POST":
        voter_id = request.POST.get('voter_id')
        password = request.POST.get('password')

        user = authenticate(request, username=voter_id, password=password)

        if user:
            login(request, user)
            voter = Voter.objects.get(voter_id=voter_id)
            request.session['voter_id'] = voter.id
            return redirect('vote')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'dreamgirl/login.html')
 
LOCATIONS = ['Doranahalli', 'Shahapur', 'Jayanagar', 'Vasantapura', 'Hosur']


# ====================================================
# 🗳 VOTE (Only 9AM–6PM)
# ====================================================

def vote(request):

    message = ""
    vote_success = False

    start, end, now = get_time()

    if now < start:
        return render(request, 'dreamgirl/vote.html', {
            'locations': LOCATIONS,
            'message': "Voting not started yet."
        })

    if now > end:
        return redirect('home')

    voter_id = request.session.get('voter_id')
    if not voter_id:
        return redirect('login')

    voter = Voter.objects.get(id=voter_id)

    selected_location = request.GET.get('location')
    candidates_by_party = {}

    if selected_location:
        candidates = Candidate.objects.filter(location=selected_location)
        for candidate in candidates:
            candidates_by_party.setdefault(candidate.party, []).append(candidate)

    # ✅ If already voted → show buttons
    if voter.has_voted:
        message = "✅ You have successfully voted."
        vote_success = True

    # 🗳 Submit vote
    if request.method == 'POST' and not voter.has_voted:

        candidate_id = request.POST.get('candidate')

        if candidate_id:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.votes += 1
            candidate.save()

            voter.has_voted = True
            voter.voted_at = timezone.now()
            voter.save()

            request.session['voter_location'] = candidate.location

            message = "✅ Your vote has been submitted successfully."
            vote_success = True

    return render(request, 'dreamgirl/vote.html', {
        'locations': LOCATIONS,
        'selected_location': selected_location,
        'candidates_by_party': candidates_by_party,
        'message': message,
        'vote_success': vote_success  # ✅ IMPORTANT
    })
# ====================================================
# 📊 LIVE RESULTS (Only Before 6PM)
# ====================================================



# ====================================================
# 🏆 FINAL RESULTS (Only After 6PM)
# ====================================================


# ====================================================
# 🔑 FORGOT PASSWORD (Blocked After 6PM)
# ====================================================

def forgot_password(request):

    start, end, now = get_time()

    if now > end:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            Voter.objects.get(email=email)
            request.session['reset_email'] = email
            return redirect('reset_password')
        except Voter.DoesNotExist:
            messages.error(request, "Email not found.")

    return render(request, 'dreamgirl/forgot_password.html')


def reset_password(request):

    start, end, now = get_time()

    if now > end:
        return redirect('home')

    email = request.session.get('reset_email')

    if not email:
        return redirect('forgot_password')

    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            voter = Voter.objects.get(email=email)
            user = User.objects.get(username=voter.voter_id)

            user.set_password(password)
            user.save()

            request.session.pop('reset_email')
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'dreamgirl/reset_password.html')


# ====================================================
# 🚪 LOGOUT
# ====================================================

def logout_view(request):
    logout(request)
    return redirect('home')


# ====================================================
# 📊 DASHBOARD (Blocked After 6PM)
# ====================================================

def dashboard(request):

    start, end, now = get_time()

    if now > end:
        return redirect('home')

    return render(request, 'dreamgirl/dashboard.html')






def results(request):

    start, end, now = get_time()

    # 🔒 After voting time → block live results
    if now > end:
        return redirect('home')

    location = request.GET.get('location')

    # If no location selected
    if not location:
        locations = Candidate.objects.values_list('location', flat=True).distinct()
        return render(request, 'dreamgirl/select_location.html', {
            'locations': locations
        })

    # Candidate results
    candidates = Candidate.objects.filter(location__iexact=location)
    total_votes = sum(c.votes for c in candidates)

    chart_names = []
    chart_votes = []
    percentage_data = []

    max_votes = max([c.votes for c in candidates]) if candidates else 0

    for c in candidates:
        chart_names.append(c.name)
        chart_votes.append(c.votes)

        percent = round((c.votes / total_votes) * 100, 2) if total_votes > 0 else 0

        percentage_data.append({
            "name": c.name,
            "party": c.party,
            "logo": c.party_logo.url if c.party_logo else "",
            "votes": c.votes,
            "percent": percent,
            "is_winner": c.votes == max_votes and total_votes > 0
        })

    return render(request, 'dreamgirl/results.html', {
        'selected_location': location,
        'chart_names': json.dumps(chart_names),
        'chart_votes': json.dumps(chart_votes),
        'percentage_data': percentage_data,
        'total_votes': total_votes,
    })



def final_results(request, location):

    start, end, now = get_time()

    # Block before result time
    if now < end:
        return render(request, 'dreamgirl/result_not_declared.html')

    # Get candidates of this location
    candidates = list(Candidate.objects.filter(location__iexact=location))

    if not candidates:
        return redirect('home')

    # Sort by votes (highest first)
    candidates.sort(key=lambda x: x.votes, reverse=True)

    total_votes = sum(c.votes for c in candidates)

    # ======================
    # TIE DETECTION
    # ======================
    max_votes = max(c.votes for c in candidates)

    top_candidates = [c for c in candidates if c.votes == max_votes]
    other_candidates = [c for c in candidates if c.votes != max_votes]

    is_tie = len(top_candidates) > 1 and max_votes > 0
    winner = None if is_tie else top_candidates[0]

    # ======================
    # Candidate UI Data
    # ======================
    colors_list = ['#22c55e', '#3b82f6', '#ef4444',
                   '#f59e0b', '#a855f7', '#06b6d4']

    all_candidates = []

    for index, c in enumerate(candidates):
        percent = round((c.votes / total_votes) * 100, 2) if total_votes > 0 else 0

        all_candidates.append({
            "name": c.name,
            "party": c.party,
            "logo": c.party_logo.url if c.party_logo else "",
            "votes": c.votes,
            "percent": percent,
            "color": colors_list[index % len(colors_list)]
        })

    # ======================
    # DEMOGRAPHICS (CORRECTED)
    # ======================

    # All registered voters in this location
    all_voters = Voter.objects.filter(location__iexact=location)

    # Only those who voted
    voted_voters = all_voters.filter(has_voted=True)

    total_registered = all_voters.count()
    total_voted = voted_voters.count()

    # Gender Count
    male_count = voted_voters.filter(gender__iexact='male').count()
    female_count = voted_voters.filter(gender__iexact='female').count()

    # Age Count
    age_18_25 = voted_voters.filter(age__gte=18, age__lte=25).count()
    age_26_40 = voted_voters.filter(age__gte=26, age__lte=40).count()
    age_40_plus = voted_voters.filter(age__gt=40).count()

    # Turnout Percentage
    turnout_percentage = round(
        (total_voted / total_registered) * 100, 2
    ) if total_registered > 0 else 0

    return render(request, 'dreamgirl/final_results.html', {
        "selected_location": location,
        "is_tie": is_tie,
        "winner": winner,
        "top_candidates": top_candidates,
        "other_candidates": other_candidates,
        "all_candidates": all_candidates,
        "total_votes": total_votes,
        "male_count": male_count,
        "female_count": female_count,
        "age_18_25": age_18_25,
        "age_26_40": age_26_40,
        "age_40_plus": age_40_plus,
        "total_registered": total_registered,
        "turnout_percentage": turnout_percentage,
    })