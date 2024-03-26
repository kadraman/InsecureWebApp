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
	<title>Fortify Demo App :: Error</title>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/bootstrap.min.css"/>">
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/fontawesome.all.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/lib/icomoon/style.css"/>"/>
	<link rel="stylesheet" type="text/css" href="<c:url value="/css/app.css"/>">
</head>

<body>

	<div id="app" class="d-flex flex-column min-vh-100 site-wrap">

		<jsp:include page="includes/header.jsp"></jsp:include>

		<!-- content -->
		<div class="site-section">
			<div class="container h-100">

                <div class="row">
                    <div class="col-md-12 text-center">
                        <span class="display-3 text-danger">
                            <i class="fa fa-exclamation-triangle" aria-hidden="true"></i>
                        </span>
                        <h2 class="display-3 text-black">Error</h2>
                        <p class="lead">We're sorry there was an error processing your request!</p>
                        <p>
                            <a class="btn btn-outline-danger" data-toggle="collapse" href="#errorDetails" role="button" aria-expanded="false">Show Details</a>
                        </p>
                        <div class="row mb-5">
                            <div class="col">
                                <div class="collapse multi-collapse" id="errorDetails">
                                    <div class="card card-body">
                                            Failed URL: ${url}
                                            Exception:  ${exception.message}
                                            <c:forEach items="${exception.stackTrace}" var="ste">
                                                ${ste}
                                            </c:forEach>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <p><a href="/" class="btn btn-md height-auto px-4 py-3 btn-primary">Back to Shop</a></p>
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
