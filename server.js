const {get_main_data,get_main_data_to_lastpage} = require("./scraping.js");
const {find_unique_seller,get_product_number_for_all_sellers} = require("./dataselecting.js")
const express = require("express");
const dotenv = require("dotenv");
dotenv.config();
const cors = require("cors");
const bodyParser = require('body-parser');
const app = express();
app.use(cors({
    origin: true,
}));
app.use(bodyParser.urlencoded({ extended: true }));
app.get("/api/data",async(req,res)=>{
    const {page} = req.query;
    console.log(req.params)
    try {
        const d = await get_main_data_to_lastpage(page);
        const allseller = find_unique_seller(d);
        const sellersanalytics = get_product_number_for_all_sellers(allseller,d);
        return res.status(200).json({data:d,allseller,sellersanalytics,message:'Data is ready for analyz'});
    } catch (error) {
        return res.status(500).json({message:error.name});
    }
})

const port = process.env.PORT || 5000;
app.listen(port,()=>{
    console.log("Server listening on port:"+port);
})