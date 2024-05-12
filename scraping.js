const axios = require('axios');
const cheerio = require('cheerio');
const {get_product_title,get_product_price_new,get_product_price_old,get_price_difference,get_product_rating,
    get_product_seller,get_monthly_paing,get_product_href} = require("./dataselecting.js");
const {productsurl} = require("./constant.js")
async function getHtmlPage(url) {
    try {
        const response = await axios.get(url);
        return response.data;
    } catch (error) {
        console.error('Error fetching page:', error);
        return null;
    }
}

function getProductsData(html) {
    const data = [];
    const $ = cheerio.load(html);
    const productsWrapper = $('.MPProductsListBannersWrapper');
    if (productsWrapper.length) {
        const products = productsWrapper.find('.MPProductItem');
        products.each((index, element) => {
            const title = get_product_title($(element));
            const pricenew = get_product_price_new($(element));
            const priceold = get_product_price_old($(element));
            const endirim = get_price_difference($(element));
            const rating = get_product_rating($(element));
            const seller = get_product_seller($(element));
            const paingdetail = get_monthly_paing($(element));
            const productlink = get_product_href($(element))
            data.push({ title, pricenew, priceold, endirim, rating, seller, paingdetail, productlink });
        });
    }
    return data;
}



async function get_main_data(page) {
    const base_url = productsurl+page;
    const html = await getHtmlPage(base_url);
    if (html) {
        const productsData = getProductsData(html);
        return productsData;
    }
    else{
        return [];
    }
}

async function get_main_data_to_lastpage(lastpage){
    let r = [];
    for(let i=1;i<=lastpage;i++){
        const d = await get_main_data(i);
        r.push(...d)
    }
    return r;
}
module.exports = {
    get_main_data,
    get_main_data_to_lastpage
}
