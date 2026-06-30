document.addEventListener('DOMContentLoaded', function () {
    const priceMin = document.getElementById('price-min');
    const priceMax = document.getElementById('price-max');
    const priceMinDisplay = document.getElementById('price-min-display');
    const priceMaxDisplay = document.getElementById('price-max-display');
    const priceRangeSelected = document.getElementById('price-range-selected');
    const minGap = 10; // Distância mínima entre os controles

    function updateSlider() {
        let minVal = parseInt(priceMin.value);
        let maxVal = parseInt(priceMax.value);

        if (maxVal - minVal < minGap) {
            if (priceMin === document.activeElement) {
                priceMin.value = maxVal - minGap;
                minVal = maxVal - minGap;
            } else {
                priceMax.value = minVal + minGap;
                maxVal = minVal + minGap;
            }
        }

        priceMinDisplay.textContent = 'R$ ' + minVal;
        priceMaxDisplay.textContent = 'R$ ' + maxVal;

        // Atualiza a barra destacada
        priceRangeSelected.style.left = (minVal / priceMin.max * 100) + '%';
        priceRangeSelected.style.width = ((maxVal - minVal) / priceMin.max * 100) + '%';
    }

    priceMin.addEventListener('input', updateSlider);
    priceMax.addEventListener('input', updateSlider);

    // Inicializa
    updateSlider();
});
