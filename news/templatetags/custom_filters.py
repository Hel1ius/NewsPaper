from django import template

register = template.Library()


@register.filter()
def censor(text):
    bad_word = ['сук', 'бл']
    text_split = text.split(' ')
    censored_text = []
    for word in text_split:
        if word.lower() in bad_word:
            censored_word = '***'
            censored_text.append(censored_word)
        else:
            censored_text.append(word)
    result = ' '.join(censored_text)
    return result

