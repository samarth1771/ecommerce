from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
from django.views.generic import ListView, DetailView, View, TemplateView
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm, CouponForm
import stripe
import random
import string

# stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choice(string.ascii_lowercase + string.digits))

def test_view(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'product-page.html', context)


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"
    paginate_by = 4


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
            }

            return render(self.request, 'payment.html', context)
        else:
            messages.error(self.request, "Complete the checkout form first")
            return redirect('core:checkout')

    def post(self, *args, **kwargs):
        # `source` is obtained with Stripe.js; see
        # https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token

        token = stripe.Token.create(
            card={
                "number": "4242424242424242",
                "exp_month": 9,
                "exp_year": 2021,
                "cvc": "314",
            },
        )

        order = Order.objects.get(user=self.request.user, ordered=False)
        # token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)
        print(order)
        print(token)
        print(amount)
        print(self.request.POST)

        # Stipe error handling

        try:
            charge = stripe.Charge.create(
                amount=amount,  # Cents
                currency="usd",
                source=token,
            )

            # Create payment

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()
            print(payment)

            # Assign payment to the order
            # Updating all items of order to ordered
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered = True
            order.payment = payment
            # TODO : assign ref code
            order.save()
            # print(order)

            messages.success(self.request, "Your order was successfully placed")
            return redirect('/')

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect('/')

            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate Limit Error")
            return redirect('/')

        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            err_msg = e.error
            messages.error(self.request, "Invalid Parameters")
            return redirect('/')

        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "You are not authenticated")
            return redirect('/')

        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network Error")
            return redirect('/')

        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(self.request, "Something went wrong. Please try again")
            return redirect('/')

        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            # Send an email to ourselves
            messages.error(self.request, "A serious error occured, We are working on it")
            return redirect('/')


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            print(order.items)
            context = {
                'object': order
            }
            return render(self.request, "order-summary.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order")
            return redirect('/')


class ItemDetialView(DetailView):
    model = Item
    template_name = "product-page.html"


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False
            )
            form = CheckoutForm()
            # Sending the form layout
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }
            return render(self.request, "checkout-page.html", context)

        except ObjectDoesNotExist:
            messages.error(self.request, "Order does not exists")
            return redirect("core:checkout")
        # order = Order.objects.get(user=self.request.user, ordered=False)

    def post(self, *args, **kwargs):
        # getting for data from GET
        # print(self.request.POST)
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip = form.cleaned_data.get('zip')
                # same_shipping_address = form.cleaned_data.get('same_shipping_address')
                # save_info = form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # print("Form is Valid")
                # print(form.cleaned_data)

                if payment_option == 'S':
                    return redirect("core:payment", payment_option='stripe')
                elif payment_option == "P":
                    return redirect("core:payment", payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid Payment Option selected")
                    return redirect("core:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any active order")
            return redirect('core:order-summary')

        messages.warning(self.request, "Failed Checkout")
        return redirect("core:checkout")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item=item,
                                                          user=request.user,
                                                          ordered=False)

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated")
            return redirect('core:order-summary')

        else:
            messages.info(request, "This item was added to your cart")
            order.items.add(order_item)
            return redirect('core:product', slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart")
        return redirect('core:order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed to your cart")
            return redirect('core:order-summary')

        else:
            # user does not have order item
            messages.info(request, "This item was not in your cart")
            return redirect('core:product', slug=slug)


    else:
        # Add a message that user has not order
        messages.info(request, "You do not have an active order")
        return redirect('core:product', slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item,
                                                  user=request.user,
                                                  ordered=False)[0]
            # if order_item.quantity == 0:
            #     order.items.remove(order_item)
            #     messages.info(request, "This item was deleted")
            #     return redirect('core:order-summary')
            # else:
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.info(request, "This item quantity was updated")
                return redirect('core:order-summary')
            else:
                order.items.remove(order_item)
                messages.info(request, "This item was deleted")
                return redirect('core:order-summary')


        else:
            # user does not have order item
            messages.info(request, "This item was not in your cart")
            return redirect('core:product')


    else:
        # Add a message that user has not order
        messages.info(request, "You do not have an active order")
        return redirect('core:product', slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon does not exists")
        # return redirect("core:order-summary")
        return None


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user,
                    ordered=False
                )
                coupon = get_coupon(self.request, code)
                if coupon:
                    order.coupon = coupon
                    order.save()
                    messages.success(self.request, "Coupon applied successfully")
                    return redirect("core:checkout")
                # messages.success(self.request, "Coupon can not be applied")
                return redirect("core:checkout")
            except Exception as e:
                messages.warning(self.request, "You don't have any active order")
                return redirect("core:checkout")
