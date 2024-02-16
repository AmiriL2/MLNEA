const openPopupBtn = document.getElementById('openPopup');
const closePopupBtn = document.getElementById('closePopup');
const popup = document.getElementById('popup');

openPopupBtn.addEventListener('click', () => {
  popup.style.display = 'block';
});

closePopupBtn.addEventListener('click', () => {
  popup.style.display = 'none';
});
