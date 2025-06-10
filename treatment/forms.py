from django import forms
from datetime import datetime

SESSION_TYPE_CHOICES = [
    ('Individual', 'Individual'),
    ('Group', 'Group'),
    ('Family', 'Family'),
    ('Telehealth', 'Telehealth'),
]
MOOD_CHOICES = [
    ('Positive', 'Positive'),
    ('Neutral', 'Neutral'),
    ('Negative', 'Negative'),
    ('Anxious', 'Anxious'),
    ('Depressed', 'Depressed'),
    ('Angry', 'Angry'),
]
SUBSTANCE_USE_CHOICES = [
    ('None', 'None'),
    ('Relapse', 'Relapse (specify substance)'),
    ('Reduced Use', 'Reduced Use'),
    ('Continued Use', 'Continued Use'),
]
PRIMARY_SUBSTANCE_CHOICES = [
    ('Opioids', 'Opioids'),
    ('Alcohol', 'Alcohol'),
    ('Stimulants', 'Stimulants'),
    ('Cannabis', 'Cannabis'),
    ('Other', 'Other (specify)'),
]
FREQUENCY_CHOICES = [
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('None', 'None'),
]
WITHDRAWAL_CHOICES = [
    ('None', 'None'),
    ('Mild', 'Mild'),
    ('Moderate', 'Moderate'),
    ('Severe', 'Severe'),
]
ADHERENCE_CHOICES = [
    ('Fully Adherent', 'Fully Adherent'),
    ('Partially Adherent', 'Partially Adherent'),
    ('Non-Adherent', 'Non-Adherent'),
    ('Not Applicable', 'Not Applicable'),
]
MENTAL_HEALTH_CHOICES = [
    ('Stable', 'Stable'),
    ('Worsening', 'Worsening'),
    ('Improving', 'Improving'),
    ('Crisis', 'Crisis'),
]
PROGRESS_CHOICES = [
    ('Significant Progress', 'Significant Progress'),
    ('Some Progress', 'Some Progress'),
    ('No Progress', 'No Progress'),
    ('Regression', 'Regression'),
]
SUPPORT_CHOICES = [
    ('Strong', 'Strong'),
    ('Moderate', 'Moderate'),
    ('Weak', 'Weak'),
    ('None', 'None'),
]
HOUSING_CHOICES = [
    ('Stable', 'Stable'),
    ('Temporary', 'Temporary'),
    ('Homeless', 'Homeless'),
    ('Other', 'Other'),
]
EMPLOYMENT_CHOICES = [
    ('Employed', 'Employed'),
    ('Unemployed', 'Unemployed'),
    ('Student', 'Student'),
    ('Retired', 'Retired'),
    ('Disabled', 'Disabled'),
]
ENGAGEMENT_CHOICES = [
    ('Highly Engaged', 'Highly Engaged'),
    ('Moderately Engaged', 'Moderately Engaged'),
    ('Minimally Engaged', 'Minimally Engaged'),
    ('Disengaged', 'Disengaged'),
]
BOOLEAN_CHOICES = [
    ('Yes', 'Yes'),
    ('No', 'No'),
]

class CounsellingSessionForm(forms.Form):
    # Stage 1
    session_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), initial=datetime.today)
    session_duration = forms.IntegerField(min_value=1, label='Session Duration (minutes)')
    session_type = forms.ChoiceField(choices=SESSION_TYPE_CHOICES)
    counselor_name = forms.CharField(max_length=100)
    patient_mood = forms.ChoiceField(choices=MOOD_CHOICES, label="Patient’s Current Mood")
    substance_use = forms.ChoiceField(choices=SUBSTANCE_USE_CHOICES, label="Substance Use Since Last Session")
    primary_substance = forms.ChoiceField(choices=PRIMARY_SUBSTANCE_CHOICES)
    frequency_of_use = forms.ChoiceField(choices=FREQUENCY_CHOICES)
    last_use_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    craving_intensity = forms.IntegerField(min_value=0, max_value=10)
    withdrawal_symptoms = forms.ChoiceField(choices=WITHDRAWAL_CHOICES)
    cows_score = forms.IntegerField(min_value=0, max_value=48, required=False)
    ciwa_ar_score = forms.IntegerField(min_value=0, max_value=67, required=False)
    medication_adherence = forms.ChoiceField(choices=ADHERENCE_CHOICES)
    barriers_to_adherence = forms.CharField(widget=forms.Textarea, required=False)
    # Stage 2
    mental_health_status = forms.ChoiceField(choices=MENTAL_HEALTH_CHOICES)
    phq9_score = forms.IntegerField(min_value=0, max_value=27, required=False)
    gad7_score = forms.IntegerField(min_value=0, max_value=21, required=False)
    suicidal_ideation = forms.ChoiceField(choices=BOOLEAN_CHOICES)
    recovery_capital = forms.IntegerField(min_value=0, max_value=60, required=False, label='Recovery Capital (BARC-10 Score)')
    treatment_goals = forms.CharField(widget=forms.Textarea, required=False)
    progress_toward_goals = forms.ChoiceField(choices=PROGRESS_CHOICES)
    coping_strategies = forms.CharField(widget=forms.Textarea, required=False)
    social_support = forms.ChoiceField(choices=SUPPORT_CHOICES)
    housing_status = forms.ChoiceField(choices=HOUSING_CHOICES)
    employment_status = forms.ChoiceField(choices=EMPLOYMENT_CHOICES)
    legal_issues = forms.ChoiceField(choices=BOOLEAN_CHOICES)
    legal_issues_details = forms.CharField(widget=forms.Textarea, required=False)
    overdose_risk_factors = forms.CharField(widget=forms.Textarea, required=False)
    naloxone_possession = forms.ChoiceField(choices=BOOLEAN_CHOICES)
    referrals_made = forms.CharField(widget=forms.Textarea, required=False)
    telehealth_access = forms.ChoiceField(choices=BOOLEAN_CHOICES)
    telehealth_barriers = forms.CharField(widget=forms.Textarea, required=False)
    patient_engagement = forms.ChoiceField(choices=ENGAGEMENT_CHOICES)
    # Stage 3
    session_summary = forms.CharField(widget=forms.Textarea, required=False)
    follow_up_plan = forms.CharField(widget=forms.Textarea, required=False)
