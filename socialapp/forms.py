from django import forms
from .models import Post,Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
    widgets = {
        'bio': forms.Textarea(attrs={'rows': 3}),
    }
    
    
class UpdateProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']  