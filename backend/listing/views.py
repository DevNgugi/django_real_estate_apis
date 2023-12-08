from wsgiref.handlers import IISCGIHandler
from rest_framework.views import APIView

from .models import Listing
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Listing


from .serializers import ListingSerializer

class ManageListingView(APIView):
    def get(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error':'Something went wrong while retrieving data'},status=status.HTTP_403_FORBIDDEN)  
            slug=request.query_params.get('slug')
            if not slug:
                Listing.objects.order_by('-date_created').filter(
                    realtor=user.email
                )
                listing_queryset=Listing.objects.order_by('-date_created').filter(realtor=user.email)
                
                listing=ListingSerializer(listing_queryset,many=True)
                
                return Response({'listings': listing.data},status=status.HTTP_200_OK)  
            
            if not Listing.objects.filter(
                realtor=user.email,
                slug=slug
            ).exists():
                return Response({'error': 'Listing not found'},status=status.HTTP_404_NOT_FOUND)
            listing=ListingSerializer(Listing.objects.get(realtor=user.email,slug=slug))
            return Response({'listing':listing.data}, status=status.HTTP_200_OK)
        except Exception as e:
                return Response({'error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

    def post(self, request):
        try:
            user = request.user
            if not user.is_realtor:
                return Response({'error':'User should be a realtor'},status=status.HTTP_400_BAD_REQUEST)  
            data = request.data
            
            slug=data['slug']
            if Listing.objects.filter(slug=slug).exists():
                return Response({'error':'Listing with this slug exists'},status=status.HTTP_400_BAD_REQUEST)                    
            
            title=data['title']
            address=data['address']
            city=data['city']
            state=data['state']
            zipcode=data['zipcode']
            description=data['description']
            bedrooms=data['bedrooms']
            bathrooms=data['bathrooms']
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']
            is_published=data['is_published']
            
        
            price=data['price']
            try:
                price = int(price)
            except:
                return Response({'error':'Invalid value for price'},status=status.HTTP_400_BAD_REQUEST)                    
            
            try:
                bedrooms = int(bedrooms)
            except:
                return Response({'error':'Invalid value for bedrooms'},status=status.HTTP_400_BAD_REQUEST)                    
            try:
                bathrooms = float(bathrooms)
            except:
                return Response({'error':'Invalid value for bathrooms'},status=status.HTTP_400_BAD_REQUEST)     
            if bathrooms <=0 or bathrooms >=10:
                bathrooms = 1.0
            bathrooms=round(bathrooms,1)
            if sale_type == 'FOR_RENT':
                sale_type = 'For Rent'
            else:
                sale_type = 'For Sale'
            if home_type == 'CONDO':
                home_type = 'Condo'
            elif home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            else:
                home_type = 'House'
            if is_published=='True':
                is_published = True
            else:
                is_published = False
                
            Listing.objects.create(
                realtor=user.email,
                title=title,
                slug=slug,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                description=description,
                price=price,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sale_type=sale_type,
                home_type=home_type,
                main_photo=main_photo,
                photo_1=photo_1,
                photo_2=photo_2,
                photo_3=photo_3,
                is_published=is_published,
                )
            return Response({'succcess':'Listing Saved'},status=status.HTTP_200_OK)                    

        except Exception as e:
            return Response({'error':str(e),},status=status.HTTP_500_INTERNAL_SERVER_ERROR)                    


class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug= request.query_params.get('slug',None)
            
            if not slug:
                return Response({'error':'Must provide slug'},status=status.HTTP_400_BAD_REQUEST)  
            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response({'error':'Published listing with this slug does not exist'},status=status.HTTP_404_NOT_FOUND)  
            listing=ListingSerializer(Listing.objects.get(slug=slug,is_published=True))
            
            return Response({'listing':listing.data},status=status.HTTP_200_OK)  
        
        except:
            return Response({'error':'Something went wrong while retrieving Listing'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  

class ListingsView(APIView):
    permission_classes=[permissions.AllowAny]
    
    def get(self, request, format=None):
        try:
            if not Listing.objects.filter(is_published=True).exists():
                return Response({'error':''},status=status.HTTP_404_NOT_FOUND)  
            listings=ListingSerializer(Listing.objects.order_by('-date_created').filter(is_published=True),many=True)
            return Response({'listings':listings.data},status=status.HTTP_200_OK)  
            
        except:
            return Response({'error':'Something went wrong while retrieving Listings'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            