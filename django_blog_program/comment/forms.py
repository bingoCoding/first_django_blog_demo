import mistune
from django import forms

from comment.models import Comment


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;', 'placeholder': '昵称'}
        ),
    )
    email = forms.CharField(
        label='邮箱',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;', 'placeholder': '邮箱'}
        ),
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': 'width: 60%;', 'placeholder': '网站'}
        ),
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Textarea(
            attrs={'class': 'form-control', 'rows': 5, 'cols': 60, 'placeholder': '请输入内容'}
        ),
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么短呢')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
