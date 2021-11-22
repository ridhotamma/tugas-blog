const logoItem = document.getElementById('logo-item')
const menuItems = document.getElementById('menu-items')
const hamburger = document.getElementById('hamburger')

const toggleNavbar = () => {
    if(window.innerWidth < 600) {
        menuItems.classList.add('hide')
        hamburger.classList.remove('hide')
    } else {
        menuItems.classList.remove('hide')
        hamburger.classList.add('hide')
    }
}

window.addEventListener('resize', toggleNavbar)