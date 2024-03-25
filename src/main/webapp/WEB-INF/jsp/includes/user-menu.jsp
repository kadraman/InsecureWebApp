<%@ page language="java" contentType="text/html; charset=ISO-8859-1" pageEncoding="ISO-8859-1" %>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>

<div>
    <div class="side-menu">
        <div class="list-group list-group-flush">
            <a class="list-group-item list-group-item-action active"
               ref="/user"><i class="fas fa-home fa-fw"></i> Home</a>
            <a class="list-group-item list-group-item-action"
               href=""><i class="fas fa-user fa-fw"></i> Profile</a>
            <a class="list-group-item list-group-item-action"
               href=""><i class="fas fa-shopping-cart fa-fw"></i> Orders </a>
            <a class="list-group-item list-group-item-action"
               href=""><i class="fas fa-envelope fa-fw"></i> Messages <span id="unread-message-count" class="badge badge-pill badge-info">0</span>
                <span class="sr-only">unread messages</span>
            </a>
        </div>
    </div>
</div>
