document.addEventListener('DOMContentLoaded', () => {
    createEditors();

    document.querySelector('body').style.backgroundColor = document.querySelector('#light-color').value;
    document.querySelector('#nav').style.backgroundColor = document.querySelector('#dark-color').value;

    // get new quote
    if (document.querySelector('#blockquote')) {
        getQuote();
        const boring = document.querySelector('#boring');
        document.querySelector('#blockquote').onmouseenter = () => {
            boring.style.visibility = 'visible';
            boring.style.animationName = 'show';
            boring.style.animationPlayState = 'running';
        }
        document.querySelector('#blockquote').onmouseleave = () => {
            boring.style.animationName = 'fade';
        }
    }
    
    if (document.querySelector('#reset-button')) {
        document.querySelector('#reset-button').style.display = 'none';
    }
    // text areas resize
    const textareas = document.querySelectorAll('textarea');
    for (let i = 0; i < textareas.length; i++) {
        textareas[i].onkeyup = resize;
        textareas[i].onkeydown = resize;
    }

})

function createEditors() {
    const editors = document.querySelectorAll('.editor');
    for (let i = 0; i < editors.length; i++) {
        var quill = new Quill('#' + editors[i].id, {
        modules: {
            toolbar: [
            [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
            ['bold', 'italic', 'underline', 'link'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }]
            ]
        },
        placeholder: 'Type some notes here...',
        theme: 'snow'
        });
    }
    
    const qls = document.querySelectorAll('.ql-editor');
    const hiddenNotes = document.querySelectorAll('.hidden-notes');
    for (let i = 0; i < qls.length; i++) {
        editors[i].onkeyup = function() {
            hiddenNotes[i].value = qls[i].innerHTML;
        }
    }
}

function addTask() {
    const form = document.querySelector('#task-form-grow');
    const button = document.querySelector('#add-task');
    
    if (form.style.display == 'none') {
        form.style.display = 'block';
        button.innerHTML = `<i class="far fa-window-close"></i>&nbsp;&nbsp;Forget it *sigh*`
        button.className = 'btn btn-outline-danger';
        document.querySelector('#new-task-title').focus();
    }
    else if (form.style.animationName == 'shrink') {
        form.style.animationName = 'grow';
        button.innerHTML = `<i class="far fa-window-close"></i>&nbsp;&nbsp;Forget it *sigh*`
        button.className = 'btn btn-outline-danger';
        document.querySelector('#new-task-title').focus();
    } 
    else {
        form.style.animationName = 'shrink';
        button.innerHTML = '<i class="far fa-plus-square"></i>&nbsp;&nbsp;Another pointless obligation, this time with detail'
        button.className = 'btn btn-outline-primary';
    }
}

function checkOff(id) {
    var bool = document.getElementById('check' + id).checked;
    const title = document.getElementById('title' + id)
    if (bool) {
        title.style.textDecoration = 'line-through';
    } else {
        title.style.textDecoration = 'none';
    }
    fetch(`check_off/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            done: bool
        }),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(result => {
        setTimeout(function() {
            if (document.getElementById('check' + id).checked) {
                const task = document.getElementById('accordion' + id);
                task.style.textDecoration = 'line-through';
                task.style.animationName = 'check-off';
                task.style.animationDuration = '.5s';
                task.style.animationFillMode = 'forwards';
                task.style.animationIterationCount = '1'; 
            } else {
                title.style.textDecoration = 'none';
            } 
        }, 750);
    })
}

function checkAll() {
    const checks = document.querySelectorAll('.task');
    for (let i = 0; i < checks.length; i++) {
        checks[i].checked = true;
        var id = checks[i].id.match(/\d/g);
        id = id.join('')
        checkOff(id);
    }
    const button = document.getElementById('clearSchedule');
    button.style.animationName = 'fade';
    button.style.animationDuration = '1.2s';
    button.style.animationFillMode = 'forwards';
    button.style.animationIterationCount = '1';
    button.style.animationPlayState = 'running';

    setTimeout(() => {
        document.querySelector('#nothing').style.display = 'block';
        document.querySelector('#clearSchedule').style.display = 'none';
    }, 1200);
    

}

function deleteTag(id) {
    const tag = document.getElementById(`tag-li-${id}`);
    tag.style.animationName = 'delete-tag';
    tag.style.animationDuration = '1s';
    tag.style.animationIterationCount = '1';
    tag.style.animationFillMode = 'forwards';

    fetch('/delete_tag', {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        }),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        }
    })

}

function deleteFriend(requestee_id, requester_id) {
    const friend = document.getElementById(`friend-${requestee_id}`);
    friend.style.animationName = 'delete-tag';
    friend.style.animationDuration = '1s';
    friend.style.animationIterationCount = '1';
    friend.style.animationFillMode = 'forwards';

    fetch('/delete_friend', {
        method: 'PUT', 
        body: JSON.stringify({
            requestee_id: requestee_id,
            requester_id, requester_id
        }),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
}



function editTag(id) {
    const tag = document.getElementById(`tag${id}`);
    const form = document.getElementById(`tag-form${id}`);
    const ok = document.getElementById(`ok${id}`);
    const cancel = document.getElementById(`cancel${id}`);
    const input = document.getElementById(`tag-input${id}`);
    const row = document.getElementById(`tag-row${id}`);
    input.value = tag.innerText;
    form.style.display = 'block';
    row.style.display = 'none';

    ok.onclick = function () {
        fetch('edit_tag', {
            method: 'PUT',
            body: JSON.stringify({
                id: id,
                name: input.value,
                color: document.getElementById(`color${id}`).value
            }),
            credentials: 'same-origin',
            headers: {
                "X-CSRFToken": getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(task => {
            form.style.display = 'none';
            tag.innerText = task[0].name;
            row.style.display = 'flex';
            document.getElementById(`tag-li-${id}`).style.backgroundColor = task[0].color;
    })
    };
    
    cancel.onclick = function () {
        row.style.display = 'flex';
        form.style.display = 'none';
    }
    input.focus();
}

function editTask(id) {
    const title = document.getElementById('title' + id);
    const titleForm = document.getElementById('title-form' + id);
    const check = document.getElementById('flush-heading' + id);
    const checks = document.querySelectorAll('.flush-heading');
    const button = document.getElementById('button' + id);
    const accordionItems = document.querySelectorAll('.accordion-item')
    
    for (let i = 0; i < accordionItems.length; i++) {
        accordionItems[i].style.backgroundColor = 'inherit';
        accordionItems[i].style.borderBottom = 'none';
    }

    if (button.className != 'accordion-button collapsed') {
        check.style.backgroundColor = '#e7f1ff';
        check.style.borderBottom = '1px solid #101b15';
        OPEN = true
    } else {
        check.style.backgroundColor = 'inherit';
        check.style.borderBottom = 'none';
        OPEN = false
    }
    titleForm.onfocus = function () {
        this.onkeyup = function() {
            title.innerText = titleForm.value;
        }
    }
    for (let i = 0; i < checks.length; i++) {
        checks[i].style.backgroundColor = 'inherit';
        checks[i].style.borderBottom = 'none';
    }
}

function getQuote() {
    const index = Math.floor(Math.random() * QUOTES.length);
    const quote = document.querySelector('#quote');
    const next = document.createElement('div');
    quote.innerText = QUOTES[index].quote;
    document.querySelector('#source').innerText = QUOTES[index].source;
}

function resize() {
    this.style.height = 'auto';
    this.style.height = `${this.scrollHeight}px`;
}

function quickAdd() {
    const task = document.querySelector('#new-task').value;
    fetch('/quick_add', {
        method: 'POST',
        body: JSON.stringify({
            task: task,
            date: document.querySelector('#date').value
        }),
        credentials: 'same-origin',
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        }
    })
    .then(response => response.json())
    .then(task => {
        reactTest(task);
    })
}

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
    return cookieValue;}

var OPEN = false;

const QUOTES = [
    {
        quote: 'Trying is the first step toward failure.',
        source: 'Homer J. Simpson'
    },
    {
        quote: "If at first you don't succeed, try, try again. Then quit. No use being a damn fool about it.",
        source: 'W.C. Fields'
    },
    {
      quote: "I'm sure the universe is full of intelligent life. It's just been too intelligent to come here.", 
      source: 'Arhur C. Clarke'
    },
    {
        quote: "Never put off till tomorrow what may be done day after tomorrow just as well.",
        source: 'Mark Twain'
    },
    {
        quote: "Procrastinate now, don't put it off.",
        source: 'Ellen DeGeneres'
    },
    {
        quote: "If it weren't for the last minute, nothing would get done.",
        source: 'Rita Mae Brown'
    },
    {
        quote: "There's a sucker born every minute",
        source: 'P.T. Barnum'
    },
    {
        quote: "No man but a blockhead every wrote except for money.",
        source: 'Samuel Johnson'
    },
    {
        quote: "Everytime a friend succeeds something inside me dies.",
        source: 'Gore Vidal'
    },
    {
        quote: "I refuse to join any club that would have me as a member",
        source: 'Groucho Marx'
    },
    {
        quote: "Not everything is a lesson. Sometimes you just fail.",
        source: 'Dwight Schrute'
    },
    {
        quote: "Success is just failure that hasn't happened yet.",
        source: 'Latrell Sprewell'
    },
    {
        quote: "Challenging yourself...is a good way to fail.",
        source: 'Dom Mazzetti'
    },
    {
        quote: "Never underestimate the power of stupid people in large groups.",
        source: 'George Carlin'
    },
    {
        quote: "Hope is the first step on the road to disappointment.",
        source: 'Cassern S. Goto'
    },
    {
        quote: "The story so far: In the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move.",
        source: 'Douglas Adams'
    },
    {
        quote: "Everyone has a purpose in life. Perhaps yours is watching television.",
        source: 'David Letterman'
    },
    {
        quote: "Everything happens for a reason. Sometimes the reason is you're stupid and make bad decisions.",
        source: 'Marlon G. Harmon'
    },
    {
        quote: "Do not take life too seriously. You will never get out of it alive.",
        source: 'Elbert Hubbard'
    },
    {
        quote: "I’ve developed a new philosophy. I only dread one day at a time.",
        source: 'Charlie Brown/Charles M. Schultz'
    }
 ];

