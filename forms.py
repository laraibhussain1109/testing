from django import forms
from .models import CampaignInquiry

PLATFORM_CHOICES = [
    ('Instagram', 'Instagram'),
    ('YouTube', 'YouTube'),
    ('Facebook', 'Facebook'),
    ('Twitter', 'Twitter'),
    ('Snapchat', 'Snapchat'),
    ('LinkedIn', 'LinkedIn'),
    ('Moj', 'Moj'),
    ('Josh', 'Josh'),
    ('Koo', 'Koo'),
    ('ShareChat', 'ShareChat'),
    ('TikTok', 'TikTok'),
]
CREATOR_TYPE_CHOICES = [
    ('Nano', 'Nano'),
    ('Micro', 'Micro'),
    ('Macro', 'Macro'),
    ('Mega', 'Mega'),
    ('Mega A+', 'Mega A+'),
    ('Celebrities', 'Celebrities'),
    ('Premium Celebrities', 'Premium Celebrities'),
]

BUDGET_CHOICES = [
    ('Can’t disclose', 'Can’t disclose'),
    ('0-3 Lakhs', '0-3 Lakhs'),
    ('3-5 Lakhs', '3-5 Lakhs'),
    ('5-10 Lakhs', '5-10 Lakhs'),
    ('10-20 Lakhs', '10-20 Lakhs'),
    ('20-50 Lakhs', '20-50 Lakhs'),
    ('50 Lakhs+', '50 Lakhs+'),
]

class CampaignInquiryForm(forms.ModelForm):
    select_influencer_platform = forms.MultipleChoiceField(
        choices=PLATFORM_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
        label="Select Influencer Platform(s)"
    )
    creator_type = forms.ChoiceField(
        choices=CREATOR_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Discover your content creators"
    )

    budget_range = forms.ChoiceField(
        choices=BUDGET_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Budget in your mind"
    )

    class Meta:
        model = CampaignInquiry
        fields = [
            'brand_name',
            'brand_email',
            'brand_contact',
            'campaign_genre',
            'sub_genre',
            'Timeline',
            'describe_your_campaign',
            'select_influencer_platform',
            'region',
            'creator_type',
            'budget_range',
        ]

        widgets = {
            'brand_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your brand name'}),
            'brand_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'brand_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your contact number'}),
            'campaign_genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter campaign genre'}),
            'sub_genre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter sub-genre'}),
            'Timeline': forms.Select(attrs={'class': 'form-control'}),
            'describe_your_campaign': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your Campaign'}),
            'region': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the region'}),
        }
