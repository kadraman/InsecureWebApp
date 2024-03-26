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

package com.opentext.app.entity;

import java.util.Objects;
import java.util.UUID;

public class Product {

	public static final String TABLE_NAME = "products";

	public UUID Id;
	public String Code;
	public String Name;
	public Integer Rating;
	public String Summary;
	public String Description;
	public String Image;
	public Float Price;
	public Boolean OnSale;
	public Float SalePrice;
	public Boolean InStock;
	public Integer TimeToStock;
	public Boolean Available;

	public UUID getId() {
		return Id;
	}

	public void setId(UUID id) {
		Id = id;
	}

	public String getCode() {
		return Code;
	}

	public void setCode(String code) {
		Code = code;
	}

	public String getName() {
		return Name;
	}

	public void setName(String name) {
		Name = name;
	}

	public Integer getRating() {
		return Rating;
	}

	public void setRating(Integer rating) {
		Rating = rating;
	}

	public String getSummary() {
		return Summary;
	}

	public void setSummary(String summary) {
		Summary = summary;
	}

	public String getDescription() {
		return Description;
	}

	public void setDescription(String description) {
		Description = description;
	}

	public String getImage() {
		return Image;
	}

	public void setImage(String image) {
		Image = image;
	}

	public Float getPrice() {
		return Price;
	}

	public void setPrice(Float price) {
		Price = price;
	}

	public Boolean getOnSale() {
		return OnSale;
	}

	public void setOnSale(Boolean onSale) {
		OnSale = onSale;
	}

	public Float getSalePrice() {
		return SalePrice;
	}

	public void setSalePrice(Float salePrice) {
		SalePrice = salePrice;
	}

	public Boolean getInStock() {
		return InStock;
	}

	public void setInStock(Boolean inStock) {
		InStock = inStock;
	}

	public Integer getTimeToStock() {
		return TimeToStock;
	}

	public void setTimeToStock(Integer timeToStock) {
		TimeToStock = timeToStock;
	}

	public Boolean getAvailable() {
		return Available;
	}

	public void setAvailable(Boolean available) {
		Available = available;
	}

	@Override
	public boolean equals(Object o) {
		if (this == o) return true;
		if (o == null || getClass() != o.getClass()) return false;
		Product product = (Product) o;
		return Id.equals(product.Id) && Code.equals(product.Code) && Name.equals(product.Name) && Rating.equals(product.Rating) && Objects.equals(Summary, product.Summary) && Objects.equals(Description, product.Description) && Objects.equals(Image, product.Image) && Price.equals(product.Price) && Objects.equals(OnSale, product.OnSale) && Objects.equals(SalePrice, product.SalePrice) && Objects.equals(InStock, product.InStock) && Objects.equals(TimeToStock, product.TimeToStock) && Objects.equals(Available, product.Available);
	}

	@Override
	public int hashCode() {
		return Objects.hash(Id, Code, Name, Rating, Summary, Description, Image, Price, OnSale, SalePrice, InStock, TimeToStock, Available);
	}

	@Override
	public String toString() {
		return "Product{" +
				"Id=" + Id +
				", Code='" + Code + '\'' +
				", Name='" + Name + '\'' +
				", Price=" + Price +
				'}';
	}
}
