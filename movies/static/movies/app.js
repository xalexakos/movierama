const sortMovies = (ordering) => {
    let url = new URL(window.location.href);
    let search_params = url.searchParams;
    search_params.delete('page');

    if (!window.location.href.includes('-' + ordering)) {
        ordering = '-' + ordering;
    }
    search_params.set('ordering', ordering);
    url.search = search_params.toString();

    window.location.href = url.toString();
};

const changePage = (page_num) => {
    let url = new URL(window.location.href);
    let search_params = url.searchParams;

    search_params.set('page', page_num);
    url.search = search_params.toString();

    window.location.href = url.toString();
};

const setActiveOrdering = () => {
    // highlight active ordering.
    let url = window.location.href;
    orderingLinks = document.getElementsByClassName("ord-btn");

    for (let i = 0; i < orderingLinks.length; i++) {
        if (url.includes(orderingLinks[i].id)) {
            orderingLinks[i].classList.add('active');

            arrow_el = orderingLinks[i].getElementsByClassName((url.includes('-')) ? 'dow-arr' : 'up-arr' );
            arrow_el[0].classList.remove('hidden');
        } else {
            orderingLinks[i].classList.remove('active');
            arrow_el = orderingLinks[i].getElementsByTagName('span');
            if (typeof(arrow_el.classList) !== 'undefined')
                arrow_el.classList.add('hidden');
        }
    }
};

window.addEventListener('load', (event) => {
    setActiveOrdering();
});