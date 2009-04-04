from django.shortcuts import render_to_response
 
def sample(request):
    return render_to_response('index.html', {})