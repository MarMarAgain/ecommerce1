from django.shortcuts import render

# To view bag contents
def view_bag(request):
    return render(request, 'bag.html')

