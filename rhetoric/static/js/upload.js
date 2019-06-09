function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken')

let getYoutubeUrl = document.getElementById('getYoutubeUrl');

getYoutubeUrl.onsubmit = function(e){
    e.preventDefault();
    let formData = new FormData();

    let url = getYoutubeUrl.getElementsByTagName("input")[0].value;

    let id = url.substring(
    parseInt(url.indexOf("v=") + 2), 
    url.length
    );
    formData.append("id", id);

    axios({
        method: 'post',
        url: '/pending',
        data: formData,
        headers: {"X-CSRFToken": csrfToken}
    })
    .then(response => {
        if(response.data === "Success"){
            formData.append("url", url);
            axios({
                method: 'post',
                url: '/review',
                data: formData,
                headers: {"X-CSRFToken": csrfToken}
            });
            window.location.href = "/commentary";
        }
        else{
            alert(response.data);
        }
    })
    .catch(ex => {
        alert('Error: check console for details');
        console.log(ex);
    })
}