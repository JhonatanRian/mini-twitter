from publications.models import Post
from django import forms


class PostModelForm(forms.models.ModelForm):

    def save(self, commit=True):
        self.instance.propertier = self.user
        post = super().save(commit=False)
        post.save()

    class Meta:
        model = Post
        fields = ['text', 'archive']
        widgets = {
            'text': forms.TextInput(
                attrs={
                    "class": "w-75 form-control",
                    "placeholder": "O que você está pensando?"
                }),
            'archive': forms.FileInput(
                attrs={
                    "class": "form-control",
                    "type": "file",
                    "id": "input_file"
                }
            ),
            }
    


class SearchForm(forms.Form):
    text = forms.CharField(label="text", required=True, max_length=255, min_length=2, widget=forms.TextInput(attrs={"class": "w-75 form-control",}))
