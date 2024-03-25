<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%@ taglib prefix="sec" uri="http://www.springframework.org/security/tags" %>

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
					<div class="col-md-12 mb-0"><a href="/">Admin</a> </div>
				</div>
			</div>
		</div>

		<!-- content -->
		<div class="site-section-sm">

			<div class="container">

				<p>Welcome to the admin page ...</p>

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
