<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>

<head>
	<meta charset="utf-8"/>
	<meta http-equiv="X-UA-Compatible" content="IE=edge"/>
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<title>Fortify Demo App</title>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/bootstrap.min.css"/>">
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/fontawesome.all.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/icomoon/style.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/app.css"/>">
</head>

<body>

<div id="app" class="d-flex flex-column min-vh-100 site-wrap">

	<jsp:include page="../includes/header.jsp"></jsp:include>

	<!-- page title -->
	<div class="bg-light py-3">
		<div class="container">
			<div class="row">
				<div class="col-md-12 mb-0"><a href="/products">Shop</a> <span class="mx-2 mb-0">/</span> <strong><c:out value="${p.name}"></c:out></strong></div>
			</div>
		</div>
	</div>

	<!-- content -->
	<div class="site-section-sm">

		<div class="container">

			<div class="row">

				<div class="col-md-5 mr-auto">
					<div class="border text-center">
						<c:choose>
							<c:when test="${not empty p.image}">
								<img src="<c:url value="/img/products/${p.image}"/>" alt="Image" class="img-fluid p-5">
							</c:when>
							<c:otherwise>
								<img src="<c:url value="/img/awaiting-image-sm.png"/>" alt="Awaiting Image" class="img-fluid p-5">
							</c:otherwise>
						</c:choose>
					</div>
					<div class="mt-4">
						<h5>Product Information</h5>
						<table class="table table-sm table-borderless">
							<tr>
								<th scope="row">Code:</th>
								<td><c:out value="${p.code}" /></td>
							</tr>
							<tr>
								<th scope="row">Manufacturer:</th>
								<td>Unknown</td>
							</tr>
							<tr>
								<th scope="row">Contents:</th>
								<td>Unspecified</td>
							</tr>
							<tr>
								<th scope="row">Date First Available:</th>
								<td><fmt:formatDate value="${dateNow}" pattern="dd MMM yyyy"></fmt:formatDate></td>
							</tr>
							<tr>
								<td colspan="2">
									<a href="<c:url value="/products/${p.id}/downloadfile/datasheet.pdf"/>">
										<i class="fas fa-download fa-fw"></i> Download Datasheet
									</a>
								</td>
							</tr>
						</table>
					</div>
				</div>
				<div class="col-md-6 item-entry">
					<h2 class="text-black"><c:out value="${p.name}" /></h2>
					<span class="product-rating">
						<c:forEach begin="1" end="${p.rating}">
							<i class="fas fa-star" style="color: cornflowerblue"> </i>
						</c:forEach>
							<c:if test="${p.rating lt 5}">
								<c:set var="start" value="${p.rating+1}"></c:set>
								<c:forEach begin="${start}" end="5">
									<i class="fas fa-star" style="color: gray"> </i>
								</c:forEach>
							</c:if>
						<span class="product-reviews pl-2"><a href="#reviews-start">Customer Reviews</a>&nbsp(<span id="review-count"><c:out value="${reviewCount}" /></span>)</span>
					</span>

					<h6 class="mt-2">Summary</h6>
					<p><c:out value="${p.summary}" /></p>
					<h6>Description</h6>
					<p><c:out value="${p.description}" /></p>

					<h5 class="price pt-2 pb-4 item-price">
						<c:choose>
							<c:when test="${p.onSale}">
								<del>
									<span>
										<fmt:formatNumber value="${p.price}" type="currency" />
									</span>
								</del>
								<span>
									&ndash;<fmt:formatNumber value="${p.salePrice}" type="currency" />
								</span>
							</c:when>
							<c:otherwise>
								<span>
										<fmt:formatNumber value="${p.price}" type="currency" />
								</span>
							</c:otherwise>
						</c:choose>
						<c:choose>
							<c:when test="${p.inStock}">
								<span class="badge badge-success">In Stock</span>
							</c:when>
							<c:otherwise>
								<span class="badge badge-danger">Out of Stock</span>
								<c:out value="In stock in ${p.timeToStock} days"></c:out>
							</c:otherwise>
						</c:choose>
					</h5>
					<div class="cart-add">
						<div class="mb-4">
							<div class="input-group mb-3" style="max-width: 180px;">
								<div class="input-group-prepend">
									<button id="quantity-minus" class="btn btn-outline-primary js-btn-minus" type="button">&minus;</button>
								</div>
								<input class="form-control text-center" value="1" id="quantity-value" readonly>
								<div class="input-group-append">
									<button id="quantity-plus" class="btn btn-outline-primary js-btn-plus" type="button">&plus;</button>
								</div>
							</div>
						</div>
						<p>
							<c:choose>
								<c:when test="${p.inStock}">
									<a id="add-to-cart" href="#" onclick="return false;" class="buy-now btn btn-sm height-auto px-4 py-3 btn-primary">Add To Cart</a>
								</c:when>
								<c:otherwise>
									<a id="add-to-cart" href="#" onclick="return false;" class="disabled buy-now btn btn-sm height-auto px-4 py-3 btn-primary">Add To Cart</a>
								</c:otherwise>
							</c:choose>
						</p>
					</div>

				</div>

			</div>

			<span id="reviews-start"></span>
			<div class="product-reviews rows">
				<h4>Customer Reviews</h4>
				<c:forEach items="${reviews}" var="r">
					<div class="col-sm-12 item mb-4">
					    <h6 class='text-dark pt-2'>Review by <em><c:out value="${r.username}" /></em> on <c:out value="${r.reviewDate}" /></h6>
					<p><c:out value="${r.comment}" /></p>
					</div>
				</c:forEach>
			</div>

		</div>

	</div>

	<jsp:include page="../includes/footer.jsp"></jsp:include>

	<script type="text/javascript" src="<c:url value="/js/lib/jquery.min.js"/>"></script>
	<script type="text/javascript" src="<c:url value="/js/lib/bootstrap.bundle.min.js"/>"></script>
	<script type="text/javascript" src="<c:url value="/js/SubscribeNewsletter.js"/>"></script>
	<script type="text/javascript" src="<c:url value="/js/app.js"/>"></script>

	<script type="text/javascript">
		(function ($) {
			$(document).ready(function () {
				$('#subscribe-newsletter').SubscribeNewsletter();
			});
		})(jQuery);
	</script>

</div>

</body>

</html>
