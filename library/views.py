


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Sector,SME, Bank, Investment
from .serializers import smeSerializer,InvestmentSerializer,SectorSerializer
import json, requests, random
from django.http import JsonResponse


class DisplaySpecificMSME(APIView):
    serializer_class = smeSerializer
    def get(self, request, id):  # Add 'id' parameter to the get method
        msmeobj = SME.objects.filter(id=id).first()
        if msmeobj is not None:
            sector_name = msmeobj.sector.name
            return Response({"sector_name": sector_name})
        else:
            return Response({"error": "SME not found"}, status=404)
        
        
        
class showMSMEDetails(APIView):
    serializer_class = smeSerializer
    def post(self, request): 
        gstn=request.data.get('gstn')
        msmeobj = SME.objects.filter(gstn=gstn).first()
        if msmeobj is not None:
            serializer = self.serializer_class(msmeobj)
            sector_name = msmeobj.sector.name
            serialized_data = serializer.data
            serialized_data['sector_name'] = sector_name
            return Response(serialized_data)
        else:
            return Response({"error": "SME not found"}, status=status.HTTP_404_NOT_FOUND)
        
        

class SMEListView(APIView):
    serializer_class = smeSerializer
    def get(self, request):
        # Get parameters from request query parameters
        askamt = request.query_params.get('askamt')
        givenamt = request.query_params.get('givenamt')
        label = request.query_params.get('label')
        amount_paid = request.query_params.get('amount_paid')

        # Filter SME objects based on parameters
        queryset = SME.objects.all()
        if askamt:
            queryset = queryset.filter(askamt=askamt)
        if givenamt:
            queryset = queryset.filter(givenamt=givenamt)
        if label:
            queryset = queryset.filter(label=label)
        if amount_paid:
            queryset = queryset.filter(amount_paid=amount_paid)

        # Serialize queryset and return response
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


        
class RegisterMSME(APIView):
    def post(self, request):
        responses = ['Secure', 'Moderate Risky',  'Most Secure', 'Most Risky', 'Risky']
        serializer = smeSerializer(data=request.data)
        if serializer.is_valid():
            gstn = request.data.get('gstn')
            askamt=request.data.get('askamt')   
            with open('library/data.json', 'r') as file:
                data = json.load(file) 
            label_api_url = 'https://cheetah-adapted-phoenix.ngrok-free.app/sme-label/'
            random_object = random.choice(data)
            print(random_object)
            response = requests.post(label_api_url, json=random_object)
            random_response = random.choice(responses)
            try:
                label_response = requests.post(label_api_url, json=data)
                if label_response.status_code == 200:
                    label = label_response.json().get('prediction')[0]
                    label=random_response
                    print(label)
                else:
                    label = None
            except Exception as e:
                label = None
            
            sector_id = request.data.get('sector')
            sector = Sector.objects.get(pk=sector_id)
            sector.total_ask+=askamt
            sector.save()
            if not SME.objects.filter(gstn=gstn).exists():
                serializer.save()
                serializer.save(label=label)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InvestmentCreateView(APIView):
    def post(self, request):
        serializer = InvestmentSerializer(data=request.data)
        if serializer.is_valid():
            investment=serializer.save()
            sector_id = request.data.get('sector')
            bank_id=request.data.get('bank')
            amount=request.data.get('amount')
            try:
                sector = Sector.objects.get(pk=sector_id)
                sector.total_amount += amount
                sector.save()
                bank = Bank.objects.get(pk=bank_id)
                bank.total_amount += amount
                bank.save()
            except Sector.DoesNotExist:
                return Response({"error": "Sector not found"}, status=status.HTTP_404_NOT_FOUND)
            
            try:
                diff=sector.total_ask- sector.total_amount
                if(diff>0):
                    ratio = sector.total_amount / sector.total_ask if sector.total_ask != 0 else 0
                    for sme in SME.objects.filter(sector=sector):
                        sme.givenamt = sme.askamt * ratio
                        sme.save()
                else:
                    return Response({"error": "Money offered higher than ask"}, status=status.HTTP_404_NOT_FOUND)
            except Sector.DoesNotExist:
                return Response({"error": "Sector not found"}, status=status.HTTP_404_NOT_FOUND)
                
            
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class SectorListView(APIView):
    serializer_class = SectorSerializer
    def get(self, request):
        sectors = Sector.objects.all()  
        serializer = self.serializer_class(sectors, many=True)
        response_data = {
            "data": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
class BankInvestmentView(APIView):
    def post(self, request):
        try:
            bank_id=request.data.get('bankid')
            bank = Bank.objects.get(pk=bank_id)
            
            total_amount = bank.total_amount
            
            investments = Investment.objects.filter(bank=bank)
            
            # Calculate total investment amount for each sector
            sector_investments = {}
            for investment in investments:
                sector_name = investment.sector.name
                total_investment = investment.amount
                if sector_name in sector_investments:
                    sector_investments[sector_name] += total_investment
                else:
                    sector_investments[sector_name] = total_investment
            
            # Format sector_investments as a list of dictionaries
            formatted_sector_investments = []
            for sector_name, total_investment in sector_investments.items():
                formatted_sector_investments.append({
                    'name': sector_name,
                    'total': total_investment
                })
            
            response_data = {
                'bank_name': bank.name,
                'total_amount': total_amount,
                'sector_investments': formatted_sector_investments
            }
            
            return JsonResponse(response_data, status=200)
        
        except Bank.DoesNotExist:
            return JsonResponse({'error': 'Bank not found'}, status=404)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)