function get_product_title(one_product_block) {
    const title = one_product_block.find('.MPTitle');
    if (title.length) {
        return title.text().trim();
    }
    return null;
}
function get_product_price_new(one_product_block) {
    const price_new = one_product_block.find('span[data-info="item-desc-price-new"]');
    if (price_new.length) {
        return price_new.text().trim();
    }
    return null;
}
function get_product_price_old(one_product_block) {
    const price_old = one_product_block.find('span[data-info="item-desc-price-old"]');
    if (price_old.length) {
        return price_old.text().trim();
    }
    return null;
}
function get_product_rating(one_product_block) {
    const rating = one_product_block.find('.Rating');
    if (rating.length) {
        return parseFloat(rating.text().trim());
    }
    return 0;
}
function get_product_seller(one_product_block) {
    const seller = one_product_block.find('.line-clamp-2');
    if (seller.length) {
        return seller?.text()?.trim()?.split(":")[1]?.trim()?.split(",")?.map(val=>val.trim());
    }
    return [];
}
function get_product_href(one_product_block) {
    const anchorElement = one_product_block.find('a');
    if (anchorElement.length) {
        const hrefValue = anchorElement.attr('href');
        return "https://umico.az"+hrefValue;
    }
    return null;
}

function find_unique_seller(data){
    const uniqueSellers = new Set();
    data.forEach(item => {
        item.seller.forEach(seller => {
            uniqueSellers.add(seller);
        });
    });
    return Array.from(uniqueSellers);
}
function get_price_difference(one_product_block) {
    const new_price_value = get_product_price_new(one_product_block);
    const old_price_value = get_product_price_old(one_product_block);
    if (new_price_value && old_price_value) {
        const new_price = parseFloat(new_price_value.replace('₼', '').replace(" ", "").trim());
        const old_price = parseFloat(old_price_value.replace('₼', '').replace(" ", "").trim());
        const price_difference = old_price - new_price;
        return price_difference;
    } else {
        return null;
    }
}

function get_monthly_paing(one_product_block){
    const monthly_paid = one_product_block.find(".MPInstallment");
    if (monthly_paid.length) {
        return monthly_paid.text().trim();
    }
    return null;
}

function get_product_number_for_each_seller(sellerName, data) {
    let s = { sellername: sellerName, numberofproduct: 0 }; 
    for (let i of data) {
        const sellers = i?.seller;
        if (sellers && sellers.includes(sellerName)) {
            s.numberofproduct++; 
        }
    }
    return s;
}

function get_product_number_for_all_sellers(sellers, data) {
    let d = [];
    for (let i of sellers) {
        d.push(get_product_number_for_each_seller(i, data));
    }
    return d;
}

module.exports = {
    get_product_title,get_product_price_new,get_product_price_old,get_price_difference,get_product_rating,
    get_product_seller,find_unique_seller,get_monthly_paing,get_product_href,get_product_number_for_all_sellers
}