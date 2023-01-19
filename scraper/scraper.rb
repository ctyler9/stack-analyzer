require "nokogiri"
require "watir"

BRANDS = ["iwc", 
    "rolex", 
    "audemarspiguet", 
    "breitling", 
    "jaegerlecoultre", 
    "omega", 
    "panerai", 
    "patekphilippe", 
    "cartier", 
    "gucci", 
    "seiko",
    "movado",
    "zenith"]


browser = Watir::Browser.new(:firefox)

BRANDS.each do |brand|
    urls = [
        "http://chrono24.com/#{brand}/index.htm",
        "http://chrono24.com/#{brand}/index-2.htm",
        "http://chrono24.com/#{brand}/index-3.htm",
        "http://chrono24.com/#{brand}/index-4.htm",
        "http://chrono24.com/#{brand}/index-5.htm"
    ]

    urls.each do |url|
        browser.goto(url)
        sleep 2
        15.times do |i|
            browser.execute_script("window.scrollBy(0,500)")
            sleep 1
        end 
        
        doc = Nokogiri::HTML.parse(browser.html)

        article_divs = doc.css(".article-item-container")
        article_divs.each do |article_div|
            image_div = article_div.at_css(".article-item-image-container .content img")
            price_div = article_div.at_css(".p-x-2 .d-flex .text-bold")
            next if !image_div || !price_div

            price_text = price_div.text
            
            image_url = image_div["src"]
            price = price_text.gsub(/[^0-9]/, "")

            puts image_url

            next if image_url.empty? || price.empty? || !image_url.start_with?("https")

            File.open("data/#{brand}.txt", "a+") do |f|
                f.puts("#{image_url},#{price}")
        end
    end

end 

end 