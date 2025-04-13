from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Product,SampleTest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np



class ProductList(APIView):
    def get(self, request):
        try:
            products = Product.objects.all()
            product_list = []
            for product in products:
                
                product_list.append({
                    'id': product.product_id,
                    'name': product.name,
                    'description': product.description,
                    'cost_price': product.cost_price,
                    'selling_price': product.selling_price,
                    'category': product.category,
                    'stock_available': product.stock_available,
                    'units_sold': product.units_sold,
                    'customer_rating': product.customer_rating,
                    'demand_forecast': product.demand_forecast,
                    'optimized_price': product.optimized_price,

                })
            return JsonResponse({'data':product_list, 'status': 200,'message': 'Products fetched successfully'})
        except Exception as e:
            print(f"Error fetching products: {e}")
            return JsonResponse({'message': 'Error fetching products', 'status': 500})
        

    def post(self, request):
        try:
            post_values = request.data
            print(post_values)
            name = post_values.get('name')
            description = post_values.get('description')
            cost_price = post_values.get('cost_price')
            selling_price = post_values.get('selling_price')
            category = post_values.get('category')
            stock_available = post_values.get('stock_available')
            units_sold = post_values.get('units_sold')
            customer_rating = post_values.get('customer_rating',0.0)
            demand_forecast = post_values.get('demand_forecast',0.0)
            optimized_price = post_values.get('optimized_price',0.0)
            
            cost_price = float(cost_price)
            selling_price = float(selling_price)
            stock_available = int(stock_available)
            units_sold = int(units_sold)

            total_units = stock_available + units_sold
            demand_forecast = units_sold + (customer_rating * 10) + (stock_available * 0.015)
            optimized_price = selling_price - (customer_rating * 0.37)

            if demand_forecast > 70:
                optimized_price *= 1.1
            elif demand_forecast < 30:
                optimized_price *= 0.9

            print(f"Optimized Price: {optimized_price}")
            # Create the product instance
            print("demand price",demand_forecast)
            product = Product.objects.create(
                name=name,
                description=description,
                cost_price=cost_price,
                selling_price=selling_price,
                category=category,
                stock_available=stock_available,
                units_sold=units_sold,
                customer_rating=customer_rating,
                demand_forecast=demand_forecast,
                optimized_price=optimized_price
            )
            product.save()
            
            return JsonResponse({
                'message': 'Product Added Successfully',
                'status': 200
            })
        except Exception as e:
            print(f"Error creating product: {e}")
            return JsonResponse({'message': 'Error creating product', 'status': 500})

class ParticularProduct(APIView):
    def get(self, request, product_id):
        try:

            product = Product.objects.get(product_id=product_id)
            product_data = {
                    'id': product.product_id,
                    'name': product.name,
                    'description': product.description,
                    'cost_price': product.cost_price,
                    'selling_price': product.selling_price,
                    'category': product.category,
                    'stock_available': product.stock_available,
                    'units_sold': product.units_sold,
                    'customer_rating': product.customer_rating,
                    'demand_forecast': product.demand_forecast,
                    'optimized_price': product.optimized_price,
            }
            return JsonResponse({'data':product_data, 'status': 200,'message': 'Product fetched successfully'})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found', 'status': 404})
        except Exception as e:
            print(f"Error fetching product: {e}")
            return JsonResponse({'message': 'Error fetching product', 'status': 500})
        
    def put(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            data = request.data
            
            # Only update fields that are provided in the request
            if 'name' in data:
                product.name = data.get('name')
            if 'description' in data:
                product.description = data.get('description')
            if 'cost_price' in data:
                product.cost_price = data.get('cost_price')
            if 'selling_price' in data:
                product.selling_price = data.get('selling_price')
            if 'category' in data:
                product.category = data.get('category')
            if 'stock_available' in data:
                product.stock_available = data.get('stock_available')
            if 'units_sold' in data:
                product.units_sold = data.get('units_sold')
            if 'customer_rating' in data:
                product.customer_rating = data.get('customer_rating')
            if 'demand_forecast' in data:
                product.demand_forecast = data.get('demand_forecast')
            if 'optimized_price' in data:
                product.optimized_price = data.get('optimized_price')
 
            product.save()
            
            return JsonResponse({'message': 'Product updated successfully', 'status': 200})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found', 'status': 404})
        except Exception as e:
            print(f"Error updating product: {e}")
            return JsonResponse({'message': 'Error updating product', 'status': 500})
        
    def delete(self, request, product_id):
        try:
            product = Product.objects.get(product_id=product_id)
            product.delete()
            return JsonResponse({'message': 'Product deleted successfully', 'status': 200})
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product not found', 'status': 404})
        except Exception as e:
            print(f"Error deleting product: {e}")
            return JsonResponse({'message': 'Error deleting product', 'status': 500})
        

    
        

