const sortMovies = (ordering) => {
    let url = new URL(window.location.href);
    let search_params = url.searchParams;
    search_params.delete('page');

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
