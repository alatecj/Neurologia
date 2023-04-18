window.onload = () => {
    myFunction2()
}

function myFunction() {
    let color_names = [["modrá", "#0000FF"], ["zelená", "#008000"], ["červená", "#FF0000"], ["žltá", "#FFFF00"],
        ["hnedá", "#964B00"], ["ružová", "#FF69B4"]]
    const get_farby = document.getElementsByClassName("farba");
    for (let i = 0; i < get_farby.length; i++) {
        const randomIndex = Math.floor(Math.random() * color_names.length);
        get_farby[i].innerText = color_names[randomIndex][0]
    }

}

function myFunction2() {
    let color_names = ["modrá", "zelená", "červená", "žltá", "hnedá", "ružová"]
    let color_codes = ["#0000FF","#008000","#FF0000","#FFD700","#964B00","#FF69B4"]
    const get_farby = document.getElementsByClassName("farba");
    for (let i = 0; i < get_farby.length; i++) {
        const randomColorName = Math.floor(Math.random() * color_names.length);
        const randomColorCode = Math.floor(Math.random() * color_codes.length);
        get_farby[i].innerText = color_names[randomColorName]
        get_farby[i].style.color = color_codes[randomColorCode]
    }

}