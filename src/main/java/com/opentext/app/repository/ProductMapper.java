/*
        FortifyDemoApp - an insecure web application.

        Copyright (C) Copyright 2024 OpenText Corp.

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

package com.opentext.app.repository;

import com.opentext.app.entity.Product;
import org.springframework.jdbc.core.RowMapper;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.UUID;

public class ProductMapper implements RowMapper<Product> {
    public Product mapRow(ResultSet rs, int rowNum) throws SQLException {
        Product product = new Product();
        product.setId(UUID.fromString(rs.getString("id")));
        product.setCode(rs.getString("code"));
        product.setName(rs.getString("name"));
        product.setRating(rs.getInt("rating"));
        product.setSummary(rs.getString(("summary")));
        product.setDescription(rs.getString("description"));
        product.setImage(rs.getString("image"));
        product.setPrice(rs.getFloat("price"));
        product.setOnSale(rs.getBoolean("on_sale"));
        product.setSalePrice(rs.getFloat("sale_price"));
        product.setInStock(rs.getBoolean("in_stock"));
        product.setTimeToStock(rs.getInt("time_to_stock"));
        product.setAvailable(rs.getBoolean("available"));
        return product;
    }
}
