import json
import requests
import os
from typing import Dict
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name="dispatch")
class AdminView(View):
    BASE_URL = os.environ["ADMIN_BASE_URL"]

    def post(self, request):
        # 1) 요청 body를 JSON으로 파싱
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # 2) 외부 Admin 서비스에 POST 요청
        try:
            resp = requests.post(self.BASE_URL, json=payload, timeout=100)
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"Admin 로그인 요청 실패: {e}"},
                status=502
            )

        # 3) 응답을 JSON으로 파싱 시도
        try:
            data = resp.json()
            # 리스트인지 판별하여 safe 플래그 설정
            is_list = isinstance(data, list)
            return JsonResponse(data, safe=not is_list, status=resp.status_code)
        except ValueError:
            # JSON이 아니면 바이트/텍스트 그대로 반환
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )


@method_decorator(csrf_exempt, name='dispatch')
class LikeProxyView(View):
    BASE_URL = os.environ["PRODUCT_BASE_URL"]

    def post(self, request, id):
        url = f'{self.BASE_URL}/{id}/like'
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        resp = requests.post(url, json=payload)
        try:
            data = resp.json()
            safe = not isinstance(data, list)
            return JsonResponse(data, safe=safe, status=resp.status_code)
        except ValueError:
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )

    def delete(self, request, id, user_id):
        if not id:
            return JsonResponse({"error": "Product id required"}, status=400)
        url = f"{self.BASE_URL}/{id}/like/{user_id}"
        resp = requests.delete(url)
        if resp.status_code == 204:
            return HttpResponse(status=204)
        return JsonResponse(resp.json(), safe=False, status=resp.status_code)

    def get(self, request, user_id):
        # 1) URL 결정: 단일 조회 vs. 전체 리스트

        url = f"{self.BASE_URL}/like/count/{user_id}"

        # 2) 외부 서비스 호출
        try:
            # request.GET.dict()로 QueryDict → 일반 dict 변환
            resp = requests.get(url, params=request.GET, timeout=100)
            resp.raise_for_status()
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"상품 서비스 요청 실패: {e}"},
                status=502
            )

        # 3) JSON 파싱을 시도
        try:
            payload = resp.json()
        except ValueError:
            # JSON이 아니면 바이너리/텍스트 그대로 반환
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get(
                    "Content-Type",
                    "application/octet-stream"
                )
            )

        # 4) JsonResponse 생성
        #    - payload가 list면 safe=False, dict면 safe=True
        is_list = isinstance(payload, list)
        return JsonResponse(
            payload,
            safe=not is_list,
            status=resp.status_code
        )


# CSRF exempt for internal microservice proxy
@method_decorator(csrf_exempt, name="dispatch")
class ProductProxyView(View):
    BASE_URL = os.environ["PRODUCT_BASE_URL"]

    def get(self, request, id=None):
        # 1) URL 결정: 단일 조회 vs. 전체 리스트
        if id is not None:
            url = f"{self.BASE_URL}/{id}"
        else:
            url = self.BASE_URL

        # 2) 외부 서비스 호출
        try:
            # request.GET.dict()로 QueryDict → 일반 dict 변환
            resp = requests.get(url, params=request.GET, timeout=100)
            resp.raise_for_status()
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"상품 서비스 요청 실패: {e}"},
                status=502
            )

        # 3) JSON 파싱을 시도
        try:
            payload = resp.json()
        except ValueError:
            # JSON이 아니면 바이너리/텍스트 그대로 반환
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get(
                    "Content-Type",
                    "application/octet-stream"
                )
            )

        # 4) JsonResponse 생성
        #    - payload가 list면 safe=False, dict면 safe=True
        is_list = isinstance(payload, list)
        return JsonResponse(
            payload,
            safe=not is_list,
            status=resp.status_code
        )

    def post(self, request, *args, **kwargs):
        # 요청 body를 JSON으로 파싱
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        resp = requests.post(self.BASE_URL, json=payload)
        try:
            data = resp.json()
            safe = not isinstance(data, list)
            return JsonResponse(data, safe=safe, status=resp.status_code)
        except ValueError:
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )


@method_decorator(csrf_exempt, name='dispatch')
class BrandLikeProxyView(View):
    BASE_URL = os.environ["BRAND_BASE_URL"]

    def post(self, request, id):
        """브랜드 좋아요"""
        url = f'{self.BASE_URL}/{id}/like'
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        resp = requests.post(url, json=payload)
        try:
            data = resp.json()
            safe = not isinstance(data, list)
            return JsonResponse(data, safe=safe, status=resp.status_code)
        except ValueError:
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )

    def delete(self, request, id, user_id):
        """브랜드 좋아요 취소"""
        if not id:
            return JsonResponse({"error": "Brand id required"}, status=400)
        url = f'{self.BASE_URL}/{id}/like/{user_id}'
        resp = requests.delete(url)
        if resp.status_code in (200, 204):
            return HttpResponse(status=resp.status_code)
        # JSON 오류날 수도 있으니 safe=False
        return JsonResponse(resp.json(), safe=False, status=resp.status_code)

    def get(self, request, user_id):
        """사용자가 좋아요한 브랜드 리스트 조회"""
        # QueryDict → dict
        params = request.GET.dict()
        url = f'{self.BASE_URL}/like/count/{user_id}'
        try:
            resp = requests.get(url, params=params, timeout=100)
            resp.raise_for_status()
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"브랜드 서비스 요청 실패: {e}"},
                status=502
            )
        try:
            payload = resp.json()
        except ValueError:
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )
        is_list = isinstance(payload, list)
        return JsonResponse(payload, safe=not is_list, status=resp.status_code)


@method_decorator(csrf_exempt, name="dispatch")
class OrderProxyView(View):
    BASE_URL = os.environ["ORDER_BASE_URL"]

    def get(self, request, user_id=None):
        # user_id가 있는 경우 (GET /order/user/{user_id})
        if not user_id:
            # 이 경우는 urls.py 설정상 호출되지 않아야 함 (또는 다른 GET 경로가 있다면 추가 로직 필요)
            return JsonResponse({"error": "user_id is required for this endpoint"}, status=400)
        
        url = f"{self.BASE_URL.rstrip('/')}/order/{user_id}"
        resp = requests.get(url, params=request.GET)

        # 2) HTTP 오류 체크
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # 하위 서비스가 4xx/5xx를 보내면 그대로 전달
            return JsonResponse(
                {"error": str(e)}, status=resp.status_code
            )

        # 3) 빈 바디(204 등) 처리
        if not resp.text:
            return JsonResponse({}, status=resp.status_code)

        # 4) Content-Type 검사
        content_type = resp.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            # JSON 아닌 경우
            return JsonResponse(
                {"error": f"Invalid Content-Type: {content_type}"},
                status=502
            )

        # 5) JSON 파싱
        try:
            data = resp.json()
        except ValueError:
            # 파싱 실패 시 빈 JSON 객체로 대응
            return JsonResponse({}, status=502)

        # 6) 리스트인지 판단해서 safe 파라미터 결정
        return JsonResponse(data, safe=False, status=resp.status_code)

    def post(self, request, *args, **kwargs):
        request_path = request.path_info
        downstream_service_path = ""

        if request_path == '/order':
            downstream_service_path = "/order"
        elif request_path == '/payment/kakao/ready':
            downstream_service_path = "/payment/kakao/ready" # 주문 서비스 내부 경로에서 /api 제거
        elif request_path == '/payment/kakao/approve':
            downstream_service_path = "/payment/kakao/approve" # 주문 서비스 내부 경로에서 /api 제거
        else:
            return JsonResponse({"error": "Invalid POST path for order/payment service"}, status=404)

        url = f"{self.BASE_URL.rstrip('/')}{downstream_service_path}"
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        resp = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
        try:
            data = resp.json()
            safe = not isinstance(data, list)
            return JsonResponse(data, safe=safe, status=resp.status_code)
        except ValueError:
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )

    def put(self, request, id=None, *args, **kwargs):
        if not id:
            return JsonResponse({"error": "Order id required"}, status=400)
        url = f"{self.BASE_URL.rstrip('/')}/order/{id}"
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        resp = requests.put(url, json=data)
        return JsonResponse(resp.json(), safe=False, status=resp.status_code)

    def delete(self, request, id=None, *args, **kwargs):
        if not id:
            return JsonResponse({"error": "Order id required"}, status=400)
        url = f"{self.BASE_URL.rstrip('/')}/order/{id}"
        resp = requests.delete(url)
        if resp.status_code == 204:
            return HttpResponse(status=204)
        return JsonResponse(resp.json(), safe=False, status=resp.status_code)


@method_decorator(csrf_exempt, name="dispatch")
class CartProxyView(View):
    BASE_URL = os.environ["CART_BASE_URL"]

    def post(self, request, user_id):
        # 1) load the raw JSON from the incoming Django request
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        # 2) forward as JSON to your cart service
        resp = requests.post(
            f"{self.BASE_URL}/{user_id}",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        return JsonResponse(resp.json(), status=resp.status_code)

    def get(self, request, user_id=None):
        if not user_id:
            return JsonResponse({"error": "user_id required"}, status=400)
        url = f"{self.BASE_URL}/{user_id}"
        resp = requests.get(
            url=url,
            json=request.GET.dict(),
            params=request.GET,
            timeout=10
        )

        return JsonResponse(resp.json(), safe=False, status=resp.status_code)

    def put(self, request, user_id=None, product_id=None):
        # 1) 필수 파라미터 체크
        if not user_id or not product_id:
            return JsonResponse(
                {"error": "user_id and product_id required"},
                status=400
            )

        # 2) JSON 파싱 ({"quantity": N})
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # 3) Cart 서비스에 PUT 요청
        url = f"{self.BASE_URL}/{user_id}/{product_id}"
        try:
            resp = requests.put(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"Cart service error: {e}"},
                status=502
            )

        # 4) FastAPI가 200 OK로 전체 카트를 반환하면 그대로 JSON 리턴
        if resp.status_code == 200:
            try:
                data = resp.json()  # ← 반드시 호출
            except ValueError:
                return HttpResponse(status=502)
            return JsonResponse(data, safe=False, status=200)

        # 5) 422 등 에러 바디가 있으면 그대로 리턴
        try:
            data = resp.json()
            return JsonResponse(data, safe=False, status=resp.status_code)
        except ValueError:
            return HttpResponse(status=resp.status_code)

    def delete(self, request, user_id=None, product_id=None):
        if not user_id:
            return JsonResponse({"error": "user_id required"}, status=400)
        path = f"/{user_id}"
        if product_id:
            path += f"/{product_id}"
        url = f"{self.BASE_URL}{path}"
        resp = requests.delete(url)
        if resp.status_code == 204:
            return HttpResponse(status=204)
        return JsonResponse(resp.json(), safe=False, status=resp.status_code)


@method_decorator(csrf_exempt, name="dispatch")
class RecommendProxyView(View):
    BASE_URL = os.environ["RECOMMEND_BASE_URL"]

    def get(self, request, user_id):
        # 1) 내부 recommend 서비스 호출 (/recommend/{user_id}?top_n=n)
        try:
            resp = requests.get(
                f"{self.BASE_URL}/{user_id}",
                params=request.GET.dict(),
                timeout=10
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return JsonResponse(
                {"error": f"Recommend 서비스 요청 실패: {e}"},
                status=502
            )

        # 2) JSON 파싱
        try:
            payload = resp.json()
        except ValueError:
            # JSON이 아닐 경우 원본 바이트/텍스트 그대로 반환
            return HttpResponse(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get("Content-Type", "application/octet-stream")
            )

        # 3) JsonResponse 생성 (dict이므로 safe=True)
        return JsonResponse(payload, safe=True, status=resp.status_code)


class AlertProxyView(View):
    BASE_URL = os.environ["ALERT_BASE_URL"]  # alert 서비스 호스트:포트/경로

    def post(self, request):
        # 1) 입력 JSON 파싱
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"detail": "Invalid JSON"}, status=400)

        # 2) alert 서비스에 POST 요청
        try:
            resp = requests.post(
                self.BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
        except requests.RequestException as e:
            return JsonResponse({"error": f"Alert service error: {e}"}, status=502)

        # 3) 응답 JSON 파싱
        try:
            data = resp.json()
        except ValueError:
            return HttpResponse(status=502)

        return JsonResponse(data,
                            safe=isinstance(data, list),
                            status=resp.status_code)

    def get(self, request, alert_id=None):
        # 경로 구성
        url = f"{self.BASE_URL}/{alert_id}" if alert_id else self.BASE_URL

        # alert 서비스 GET 요청
        try:
            resp = requests.get(url, params=request.GET, timeout=5)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Alert service error: {e}"}, status=502)

        # JSON 파싱
        try:
            data = resp.json()
        except ValueError:
            return HttpResponse(status=502)

        return JsonResponse(data,
                            safe=isinstance(data, list),
                            status=resp.status_code)

    def put(self, request, alert_id=None):
        # alert_id 필수 체크
        if not alert_id:
            return JsonResponse({"error": "alert_id required"}, status=400)

        # JSON 파싱
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        # alert 서비스에 PUT 요청
        try:
            resp = requests.put(
                f"{self.BASE_URL}/{alert_id}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
        except requests.RequestException as e:
            return JsonResponse({"error": f"Alert service error: {e}"}, status=502)

        # JSON 파싱
        try:
            data = resp.json()
        except ValueError:
            return HttpResponse(status=502)

        return JsonResponse(data,
                            safe=isinstance(data, list),
                            status=resp.status_code)

    def delete(self, request, alert_id=None):
        # alert_id 필수 체크
        if not alert_id:
            return JsonResponse({"error": "alert_id required"}, status=400)

        # DELETE 요청
        try:
            resp = requests.delete(f"{self.BASE_URL}/{alert_id}", timeout=5)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Alert service error: {e}"}, status=502)

        # 204 No Content
        if resp.status_code in (200, 204):
            return HttpResponse(status=resp.status_code)

        # 에러 바디 JSON 파싱
        try:
            data = resp.json()
            return JsonResponse(data, safe=False, status=resp.status_code)
        except ValueError:
            return HttpResponse(status=resp.status_code)

# 환경 변수에서 Promotion Service 기본 URL 로드
PROMOTION_SERVICE_BASE_URL_FROM_ENV = os.environ.get("PROMOTION_SERVICE_BASE_URL")

# PROMOTION_SERVICE_BASE_URL_FROM_ENV는 프로모션 FastAPI 서비스의 루트 URL을 가리켜야 합니다.
# 예: http://localhost:8009 또는 Docker 환경의 경우 http://promotion-service:8009
# PromotionProxyView는 이 BASE_URL에 '/promotion/' 등을 추가하여 실제 서비스 엔드포인트를 호출합니다.
@method_decorator(csrf_exempt, name="dispatch")
class PromotionProxyView(View):
    BASE_URL = PROMOTION_SERVICE_BASE_URL_FROM_ENV

    def get(self, request, promotion_id=None, action=None):
        if not self.BASE_URL:
            return JsonResponse({"error": "Promotion service URL not configured"}, status=503)

        # URL 경로 조합: BASE_URL + SERVICE_PATH_PREFIX + (action or promotion_id)
        # 예: http://localhost:8009/promotion/active/
        # 예: http://localhost:8009/promotion/<promotion_id>
        if action == "active":
            # Gateway URL: /promotion/active/
            # Downstream URL: {BASE_URL}/promotion/active/
            url = f"{self.BASE_URL.rstrip('/')}/active"
        elif promotion_id:
            # Gateway URL: /promotion/<promotion_id>/
            # Downstream URL: {BASE_URL}/promotion/<promotion_id>
            url = f"{self.BASE_URL.rstrip('/')}/{promotion_id}"
        # FastAPI 서비스에는 현재 GET /promotion/ (전체 목록) 엔드포인트가 정의되어 있지 않습니다.
        # 만약 해당 기능이 필요하다면 FastAPI 서비스에 추가 후 여기에 로직을 반영해야 합니다.
        else:
            return JsonResponse({"error": "Invalid GET path for promotion service. Use /active/ or /<promotion_id>."}, status=404)

        # 필요한 헤더 (기존 코드 스타일 참고)
        headers = {"Accept": "application/json"}
        # auth_header = request.headers.get('Authorization')
        # if auth_header:
        #     headers['Authorization'] = auth_header
        # 필요한 다른 X-Custom-Header 등도 여기서 추가 가능

        try:
            resp = requests.get(url, params=request.GET.dict(), headers=headers, timeout=10) # 타임아웃 증가
            resp.raise_for_status() # 4xx, 5xx 에러 시 예외 발생
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return JsonResponse(error_data, status=e.response.status_code, safe=not isinstance(error_data, list))
            except (ValueError, json.JSONDecodeError):
                return HttpResponse(e.response.content, status=e.response.status_code, content_type=e.response.headers.get("Content-Type"))
        except requests.RequestException as e:
            return JsonResponse({"error": f"Promotion service request (GET) failed: {e}"}, status=502)

        if resp.status_code == 204: # No Content
            return HttpResponse(status=204)
        if not resp.content and resp.status_code // 100 == 2: # 2xx 성공인데 내용이 없는 경우
             return HttpResponse(status=resp.status_code)
            
        try:
            data = resp.json()
            return JsonResponse(data, safe=not isinstance(data, list), status=resp.status_code)
        except (ValueError, json.JSONDecodeError): # 응답이 JSON이 아닐 수 있음
            return HttpResponse(
                resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type")
            )

    def post(self, request, promotion_id=None, action=None):
        if not self.BASE_URL:
            return JsonResponse({"error": "Promotion service URL not configured"}, status=503)

        # Gateway URL: /promotion/ (POST)
        # Downstream URL: {BASE_URL}/promotion/
        if promotion_id is None and action is None:
            url = f"{self.BASE_URL.rstrip('/')}{self.SERVICE_PATH_PREFIX}/"
        else:
            return JsonResponse({"error": "Invalid POST path for promotion service. Use base path for creation."}, status=404)
        
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # 필요한 경우 인증 헤더 등 추가

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return JsonResponse(error_data, status=e.response.status_code, safe=not isinstance(error_data, list))
            except (ValueError, json.JSONDecodeError):
                return HttpResponse(e.response.content, status=e.response.status_code, content_type=e.response.headers.get("Content-Type"))
        except requests.RequestException as e:
            return JsonResponse({"error": f"Promotion service request (POST) failed: {e}"}, status=502)

        if resp.status_code == 204:
            return HttpResponse(status=204)
        if not resp.content and resp.status_code // 100 == 2:
             return HttpResponse(status=resp.status_code)

        try:
            data = resp.json()
            return JsonResponse(data, safe=not isinstance(data, list), status=resp.status_code)
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(
                resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type")
            )

    def patch(self, request, promotion_id=None): # FastAPI는 PATCH를 사용하므로 put -> patch
        if not self.BASE_URL:
            return JsonResponse({"error": "Promotion service URL not configured"}, status=503)
        if not promotion_id:
            return JsonResponse({"error": "Promotion ID is required for PATCH operation."}, status=400)

        # Gateway URL: /promotion/<promotion_id>/ (PATCH)
        # Downstream URL: {BASE_URL}/promotion/<promotion_id>
        url = f"{self.BASE_URL.rstrip('/')}{self.SERVICE_PATH_PREFIX}/{promotion_id}"
        
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        # 필요한 경우 인증 헤더 등 추가

        try:
            resp = requests.patch(url, json=payload, headers=headers, timeout=10) # Changed to patch
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return JsonResponse(error_data, status=e.response.status_code, safe=not isinstance(error_data, list))
            except (ValueError, json.JSONDecodeError):
                return HttpResponse(e.response.content, status=e.response.status_code, content_type=e.response.headers.get("Content-Type"))
        except requests.RequestException as e:
            return JsonResponse({"error": f"Promotion service request (PUT) failed: {e}"}, status=502)

        if resp.status_code == 204:
            return HttpResponse(status=204)
        if not resp.content and resp.status_code // 100 == 2:
             return HttpResponse(status=resp.status_code)
            
        try:
            data = resp.json()
            return JsonResponse(data, safe=not isinstance(data, list), status=resp.status_code)
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(
                resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type")
            )

    def delete(self, request, promotion_id=None):
        if not self.BASE_URL:
            return JsonResponse({"error": "Promotion service URL not configured"}, status=503)
        if not promotion_id:
            return JsonResponse({"error": "Promotion ID is required for DELETE operation."}, status=400)

        # Gateway URL: /promotion/<promotion_id>/ (DELETE)
        # Downstream URL: {BASE_URL}/promotion/<promotion_id>
        url = f"{self.BASE_URL.rstrip('/')}{self.SERVICE_PATH_PREFIX}/{promotion_id}"
        
        headers = {"Accept": "application/json"}
        # 필요한 경우 인증 헤더 등 추가

        try:
            resp = requests.delete(url, headers=headers, timeout=10)
            # 204 No Content는 성공이므로 raise_for_status()에서 예외 발생 안 함
            # 만약 다른 2xx 성공 코드를 사용한다면 그에 맞게 처리
            if resp.status_code not in [200, 202, 204]: # 204 외 다른 성공 코드도 있을 수 있음
                 resp.raise_for_status() # 204가 아닌 다른 에러 코드에 대해서만 예외 발생
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                return JsonResponse(error_data, status=e.response.status_code, safe=not isinstance(error_data, list))
            except (ValueError, json.JSONDecodeError):
                return HttpResponse(e.response.content, status=e.response.status_code, content_type=e.response.headers.get("Content-Type"))
        except requests.RequestException as e:
            return JsonResponse({"error": f"Promotion service request (DELETE) failed: {e}"}, status=502)

        if resp.status_code == 204: # 성공적인 삭제 (No Content)
            return HttpResponse(status=204)
        
        if not resp.content and resp.status_code // 100 == 2:
             return HttpResponse(status=resp.status_code)

        # 삭제 후 다른 응답이 올 수도 있음 (예: 삭제된 객체 정보 반환 등)
        try:
            data = resp.json()
            return JsonResponse(data, safe=not isinstance(data, list), status=resp.status_code)
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(
                resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type")
            )

# TrackingProxyView도 이전 답변에서 제공한 형태로 유지 (BASE_URL이 전체 경로 포함)
@method_decorator(csrf_exempt, name="dispatch")
class TrackingProxyView(View):
    BASE_URL = os.environ.get("TRACKING_SERVICE_BASE_URL") # 예: 'http://.../log/event'

    def post(self, request):
        if not self.BASE_URL:
            return JsonResponse({"error": "Tracking service URL not configured"}, status=503)
        url = self.BASE_URL # BASE_URL 자체가 전체 엔드포인트 URL

        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=5)
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # ... (에러 처리) ...
            try:
                error_data = e.response.json(); return JsonResponse(error_data, status=e.response.status_code, safe=not isinstance(error_data, list))
            except (ValueError, json.JSONDecodeError):
                return HttpResponse(e.response.content, status=e.response.status_code, content_type=e.response.headers.get("Content-Type"))
        except requests.RequestException as e:
            return JsonResponse({"error": f"Tracking service request failed: {e}"}, status=502)
        # ... (응답 처리) ...
        if resp.status_code == 204: return HttpResponse(status=204)
        if not resp.content and resp.status_code // 100 == 2: return HttpResponse(status=resp.status_code)
        try:
            data = resp.json(); return JsonResponse(data, safe=not isinstance(data, list), status=resp.status_code)
        except (ValueError, json.JSONDecodeError):
            return HttpResponse(resp.content, status=resp.status_code, content_type=resp.headers.get("Content-Type"))