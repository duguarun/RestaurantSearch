from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyzomato import Pyzomato
import json


# Create your views here.

def home(request):
    return render(request, 'Restaurant_Search/index.html')

@csrf_exempt
def searchRestaurant(request):
    p = Pyzomato('c5515b949415a90fe3c9dfebf2d1b246')
    if request.GET.get('city', False) or request.GET.get('search', False):
        city = request.GET["city"]
        search_key = request.GET["search"]


        city = p.getLocations("query="+str(city))
        res_id = [] 
        data = {}

        search_results = p.search(entity_id=city['location_suggestions'][0]['entity_id'], entity_type=city['location_suggestions'][0]['entity_type'] ,q=search_key)
        # print(search_results['restaurants'][0]['restaurant']['R']['res_id'],search_results['restaurants'][1]['restaurant']['R']['res_id'])
        # search_results = p.search(entity_id=city['location_suggestions'][id]['entity_id'], entity_type=city['location_suggestions'][id]['entity_type'] ,q=search_key)
        try:
            for id in range(0,10):
                resta_id = search_results['restaurants'][id]['restaurant']['R']['res_id']
                name = search_results['restaurants'][id]['restaurant']['name']
                cusine = search_results['restaurants'][id]['restaurant']['cuisines']
                rating = search_results['restaurants'][id]['restaurant']['user_rating']['aggregate_rating']
                data[resta_id]={}
                data[resta_id]['name'] = name
                data[resta_id]['cusine'] = cusine
                data[resta_id]['rating'] = rating
                res_id.append(resta_id)
                data
        except:
            status = 'failed'
        else:
            status = 'success'
        if status=='success':
            return render(request, 'Restaurant_Search/SearchResults.html',{'res_id':res_id, 'data':data,'city':request.GET["city"],'search_key':search_key} )
        if status=='failed':
            return render(request, 'Restaurant_Search/SearchResults.html',{'res_id':res_id, 'data':data,'city':request.GET["city"],'search_key':search_key,'no_results':'no_results'} )

    elif request.GET.get('res_id', False):
        res_id = request.GET["res_id"]
        data = p.getRestaurantDetails(restaurant_id=res_id)
        html = ""
        html += "<p>Name: </p>"
        
        print(data['name'])
        data
        return JsonResponse (data)

