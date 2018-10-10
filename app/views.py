from django.views.generic.base import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.parsers import JSONParser
from rest_framework import status


from app.models import Machine, Wallet


@method_decorator(csrf_exempt, name="dispatch")
class GetTokenView(View):

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            machine = Machine.objects.get(name=data["name"])
            password = data["password"]

            if check_password(password, machine.password):
                token = machine.create_new_token()
                # return new token
                return JsonResponse({"token": token}, status=status.HTTP_200_OK)
            else:
                # If wrong pass
                return JsonResponse({"message": "Bad password."}, status=status.HTTP_404_NOT_FOUND)
        except Machine.DoesNotExist:
            return JsonResponse({"message": "Machine not found."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError:
            return JsonResponse({"message": "Wrong request data."}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class SetPasswordView(View):
    """Set your password"""
    def post(self, request):
        data = JSONParser().parse(request)
        try:
            password = data["password"]
            request.machine.password = make_password(password, salt=None, hasher='pbkdf2_sha256')
            request.machine.save()
            return JsonResponse({"message": "Password was updated."}, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({"message": "Wrong request data."}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class CheckPasswordView(View):
    """Check your password"""

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            password = data["password"]
            if check_password(password, request.machine.password):
                return JsonResponse({"message": "Password correct."}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "Password incorrect."}, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({"message": "Wrong request data."}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateWalletView(View):
    """Update Wallets by request.machine"""

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            wallet_list = Wallet.objects.filter(machine=request.machine)
            units_amount_dict = {
                "50 pound": 5000,
                "20 pound": 2000,
                "10 pound": 1000,
                "5 pound": 500,
                "2 pound": 200,
                "1 pound": 100,
                "50 pence": 50,
                "20 pence": 20,
                "10 pence": 10,
                "5 pence": 5,
                "2 pence": 2,
                "1 pence": 1,
            }

            for item in data:
                wallet = wallet_list.get(units=units_amount_dict.get(item))
                setattr(wallet, "amount", data.get(item))
                wallet.save()

            return JsonResponse({
                "message": "Wallets are updated."}, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({
                "message": "Wrong data request! Wallets are not updated."}, status=status.HTTP_403_FORBIDDEN)


@method_decorator(csrf_exempt, name="dispatch")
class CreateMachineView(View):
    """Create New Machine"""

    def post(self, request):
        data = JSONParser().parse(request)
        try:
            machine = Machine.objects.create(
                name=data["name"]
            )
            password = data["password"]
            machine.password = make_password(password, salt=None, hasher='pbkdf2_sha256')
            machine.save()

            list_wallet = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000]
            for i in list_wallet:
                Wallet.objects.create(machine=machine, units=i)

            return JsonResponse({
                "message": "Machine was created with name {}.".format(data["name"])
            }, status=status.HTTP_201_CREATED)
        except:
            return JsonResponse({"message": "Wrong data request."}, status=status.HTTP_403_FORBIDDEN)


@method_decorator(csrf_exempt, name="dispatch")
class SendMoneyView(View):
    """
    GET method return info by request.machine Wallets

    POST method must have dict() with "sent_money" key and in this dict must be values like:
            {"1 pound": 1,
            "20 pence": 1}
    ["50 pound", "20 pound", "10 pound", "5 pound", "2 pound", "1 pound",
    "50 pence", "20 pence", "10 pence", "5 pence", "2 pence", "1 pence"]
    """

    def get(self, request):
        wallet_machine = Wallet.objects.filter(machine=request.machine).order_by("units")

        wallet = dict()
        for i in wallet_machine:
            wallet[i.get_units_display()] = i.amount

        return JsonResponse({"Wallet": wallet}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            wallet_machine = Wallet.objects.filter(machine=request.machine)
            data = JSONParser().parse(request)
            sent_money = data["send_money"]

            total_amount_sent = 0

            units_amount_dict = {
                "50 pound": 5000,
                "20 pound": 2000,
                "10 pound": 1000,
                "5 pound": 500,
                "2 pound": 200,
                "1 pound": 100,
                "50 pence": 50,
                "20 pence": 20,
                "10 pence": 10,
                "5 pence": 5,
                "2 pence": 2,
                "1 pence": 1,
            }

            # add money to wallets
            for i in sent_money:
                wallet = wallet_machine.get(units=units_amount_dict.get(i))
                wallet.amount += sent_money[i]
                wallet.save()

                sent_amount = units_amount_dict.get(i) * sent_money[i]
                total_amount_sent += sent_amount

            # get more bigger currency unit
            cash_back = dict()
            amount = total_amount_sent

            list_item = ['50 pound', '20 pound', '10 pound', '5 pound', '2 pound', '1 pound',
                         '50 pence', '20 pence', '10 pence', '5 pence', '2 pence', '1 pence']

            for i in list_item:
                if units_amount_dict[i] <= amount:
                    units_pcs = amount // units_amount_dict[i]

                    wallet = wallet_machine.get(units=units_amount_dict.get(i))
                    # if wallet has pcs currency_unit
                    if wallet.amount >= units_pcs:

                        # Wallet minus unit pcs
                        wallet.amount -= units_pcs
                        wallet.save()

                        cash_back[i] = units_pcs
                        amount -= (units_amount_dict.get(i)*units_pcs)

            return JsonResponse({
                "total amount": total_amount_sent,
                "cash back": cash_back
            }, status=status.HTTP_200_OK)
        except KeyError:
            return JsonResponse({
                "message": "Wrong data request!"
            }, status=status.HTTP_403_FORBIDDEN)
