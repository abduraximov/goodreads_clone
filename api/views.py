from django.views import View
from Goodreads.models import BookReview
from django.http.response import JsonResponse
from rest_framework.views import APIView
from .serializers import BookReviewSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import status

class BookReviewDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        review = BookReview.objects.get(id=id)

        # json_parse = {
        #     "id": review.id,
        #     "stars_given": review.stars_given,
        #     "comment": review.comment,
        #     "book": {
        #         "id": review.book.id,
        #         "title": review.book.title,
        #         "description": review.book.description,
        #         "isbn": review.book.isbn,
        #         "cover_pic": review.book.cover_picture.url
        #     }
        # }
        # return JsonResponse(json_parse)
        serializer = BookReviewSerializer(review)
        return Response(data=serializer.data)
    
    def delete(self, request, id):
        review = BookReview.objects.get(id=id)
        review.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, id):
        review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializer(instance=review, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        review = BookReview.objects.get(id=id)
        serializer = BookReviewSerializer(instance=review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookReviewListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = BookReview.objects.all().order_by("-created_at")

        paginator = PageNumberPagination()
        page_obj = paginator.paginate_queryset(reviews, request)

        serializer = BookReviewSerializer(page_obj, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        serializer = BookReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)