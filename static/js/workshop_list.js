// Updates the main workshop detail section with the content of a clicked workshop item
document.addEventListener('DOMContentLoaded', () => {
    const workshopItems = document.querySelectorAll('.workshop-item');
    const mainWorkshopTitle = document.querySelector('.workshop-detail .workshop-title');
    const mainWorkshopSubtitle = document.querySelector('.workshop-detail .workshop-subtitle');
    const mainWorkshopPrice = document.querySelector('.workshop-detail .workshop-price');
    const mainWorkshopDescription = document.querySelector('.workshop-detail .workshop-description');
    const mainWorkshopImage = document.querySelector('.workshop-detail .workshop-image');

    // Update main workshop content
    const updateMainWorkshop = (item) => {
        const title = item.querySelector('.workshop-name').textContent;
        const subtitle = item.querySelector('.workshop-category').textContent;
        const price = item.querySelector('.workshop-price').textContent;
        const description = item.querySelector('.workshop-description').textContent;
        const imageSrc = item.querySelector('img').src;

        mainWorkshopTitle.textContent = title;
        mainWorkshopSubtitle.textContent = subtitle;
        mainWorkshopPrice.textContent = price;
        mainWorkshopDescription.innerHTML = `About<br>${description}`;
        mainWorkshopImage.src = imageSrc;
        mainWorkshopImage.alt = title;
    };

    // Event listeners for workshop items
    workshopItems.forEach(item => {
        item.addEventListener('click', () => updateMainWorkshop(item));
    });
});

