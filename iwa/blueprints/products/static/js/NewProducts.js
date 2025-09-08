/*
        InsecureWebApp - an insecure Python/Flask Web application

        Copyright (C) 2024-2025  Kevin A. Lee (kadraman)

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

$.fn.NewProducts = function (options) {
    return this.each(function (index, el) {

        var defaults = $.extend({
            limit: 3,
            currencySymbol: "&dollar;"
        });
        options = $.extend(defaults, options);

        var $this = $(this), $data = $this.find('#product-data');
        _getProducts(options.limit).then(response => {
            $data.empty();
            if (response.length > 0) {
                $.each(response, function (i, row) {
                    product = _productDiv(row);
                    $data.append(product);
                });
            } else {
                $data.append("<div class='col-12 text-center'>No products found</div>");
            }
        });
    });

    function _productDiv(product) {
        return (
            "<div class='col-sm-6 col-lg-4 text-center item mb-4'>" +
            (product.onSale ? "<span class='tag'>Sale</span>" : "") +
            "<a href='/products/" + product.code + "/view'>" +
            (product.image ? "<img src='/static//img/products/" + product.image + "' alt='Image' class='img-fluid'" : "<img src='/static//img/products/awaiting-image-sm.png' alt='Image' class='img-fluid'>") +
            "</a>" +
            "<h3 class='text - dark'><a href='/products/" + product.code + "/view'>" + product.name + "</a></h3>" +
            (product.onSale ? "<p class='price'><del>" + options.currencySymbol + Number(product.price).toFixed(2) + "</del> &mdash; " + options.currencySymbol + Number(product.salePrice).toFixed(2) + "</p>" : "<p class='price'>" + options.currencySymbol + Number(product.price).toFixed(2) + "</p>") +
            "</div>"
        );
    }

    async function _getProducts(limit) {
        return await $.get(`/api/new-products?limit=${limit}`).then();
    }

};