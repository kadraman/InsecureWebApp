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

		<jsp:include page="includes/header.jsp"></jsp:include>

		<!-- page title -->
		<div class="bg-light py-3">
			<div class="container">
				<div class="row">
					<div class="col-md-12 mb-0"><a href="/">Shop</a> </div>
				</div>
			</div>
		</div>

		<!-- content -->
		<div class="site-section-sm">

			<div class="container">

				<c:if test="${haveKeywords}">
					<div class="row pt-2">
						<div class="col-md-12 text-center">
							<h2>Searching for:
								<span class="bg-light text-dark"><span id="search-keywords"><%= request.getParameter("keywords") %></span>
							</h2>
						</div>
					</div>
				</c:if>

				<!-- search box -->
				<div class="row d-flex justify-content-center">
					<form id="search" class="col-md-10" action="#" method="GET">
						<div class="card p-3 py-4">
							<div class="row g-3 mt-2">
								<div class="input-group">
									<div class="col-md-3">
										<div class="dropdown"> <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-expanded="false"> Category </button>
											<ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
												<li><a class="dropdown-item" href="#">Vitamins & supplements</a></li>
												<li><a class="dropdown-item" href="#">Skincare</a></li>
												<li><a class="dropdown-item" href="#">Electricals</a></li>
												<li><a class="dropdown-item" href="#">Health & wellbeing</a></li>
											</ul>
										</div>
									</div>
									<div class="col-md-6">
										<input type="text" class="form-control" placeholder="Enter search keywords" name="keywords"
											   id="keywords-search-input" value="<%= request.getParameter("keywords") != null ? request.getParameter("keywords") : "" %>"/>
									</div>
									<div class="col-md-3">
										<button id="keywords-search-button" class="btn btn-secondary btn-block" type="submit">Search</button>
									</div>
								</div>
							</div>
							<div class="mt-3"> <a data-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample" class="advanced"> Advance Search With Filters <i class="fa fa-angle-down"></i> </a>
								<div class="collapse" id="collapseExample">
									<div class="card card-body">
										<div class="row">
											<div class="col-md-4"> <input type="text" placeholder="Product ID" class="form-control"> </div>
											<div class="col-md-4"> <input type="text" class="form-control" placeholder="Medical Condition"> </div>
											<div class="col-md-4"> <input type="text" class="form-control" placeholder="Search by Brand"> </div>
										</div>
									</div>
								</div>
							</div>
						</div>
					</form>
				</div>

				<div class="row pt-5">
					<c:forEach items="${products}" var="p">
						<div class="col-sm-6 col-lg-4 text-center item mb-4">
							<c:choose>
								<c:when test="${p.onSale}">
									<span class="tag">Sale</span>
								</c:when>
							</c:choose>
							<a href="<c:url value="/products/${p.id}"/>">
								<c:choose>
									<c:when test="${not empty p.image}">
										<img src="<c:url value="/img/products/${p.image}"/>" alt="Image" class="img-thumbnail">
									</c:when>
									<c:otherwise>
										<img src="<c:url value="/img/awaiting-image-sm.png"/>" alt="Awaiting Image" class="img-thumbnail">
									</c:otherwise>
								</c:choose>
							</a>
							<h3 class="text-dark"><a href="#"><c:out value="${p.name}" /></a></h3>
							<p class="price">
								<c:choose>
									<c:when test="${p.onSale}">
										<del>
											<span>
												<fmt:formatNumber value="${p.price}" type="currency" />
											</span>
										</del>
										<span>&ndash;</span>
										<span>
											<fmt:formatNumber value="${p.salePrice}" type="currency" />
										</span>
									</c:when>
									<c:otherwise>
										<span>
											<fmt:formatNumber value="${p.price}" type="currency" />
										</span>
									</c:otherwise>
								</c:choose>
							</p>
						</div>
					</c:forEach>

				</div>

				<div class="row pt-4">
					<div class="col-md-12">
						<c:choose>
							<c:when test="${haveKeywords}">
								<h5>Showing <span><c:out value="${productsCount}"/></span> of <span><c:out value="${productsTotal}"/></span> products</h5>
							</c:when>
							<c:otherwise>
								<h5>Showing <span><c:out value="${productsCount}"></c:out> products</span></h5>
							</c:otherwise>
						</c:choose>
					</div>
				</div>

			</div>

		</div>

		<jsp:include page="includes/footer.jsp"></jsp:include>

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
