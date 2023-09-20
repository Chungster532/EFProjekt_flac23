const toggleBtn = document.getElementsByClassName('toggle-btn')[0]
const navbarLinks = document.getElementsByClassName('header-right')[0]

toggleBtn.addEventListener('click', () => {
    navbarLinks.classList.toggle('active')
})