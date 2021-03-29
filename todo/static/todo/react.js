function reactTest(task) {
    if (task) {
        class Task extends React.Component {

            render() { 
                return (
                    <div className="accordion-item" id={accordionID}>
                        <h2 className="accordion-header">
                            <input id={checkID} type="checkbox" className="form-check-input task">
                            </input>
                            <button className="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target={flushCollapse}>
                                <div id={titleID}>
                                    {this.props.title}
                                </div>
                                <div className="badge">
                                    {this.props.tag}
                                </div>
                            </button>
                        </h2>
                        <div id={flushCollapseID} className="accordion-collapse collapse" data-bs-parent="#accordion">
                            <div className="accordion-body">
                                <form action={formSubmit} method="post">
                                    Title:
                                    <div className="input-group">
                                        <input id={titleForm} className="form-control" type="text" name="title" defaultValue={task.title}>
                                        </input>
                                        <a className="btn btn-outline-primary" href={task.id}>Open as page</a>
                                    </div>
                                    Notes:
                                    <div id={editorID} className="editor">

                                    </div>
                                    <input name="description" type="text" className="hidden-notes">
                                    </input>
                                    <div className="input-group">
                                        <span className="input-group-text"><i className="fas fa-share-square"></i></span>
                                        <input name="recipient" className="form-control" placeholder="username" autoComplete="off" defaultValue=''>
                                        </input>
                                        <span className="input-group-text"><i className="fas fa-tag"></i></span>
                                        <input name="tag" className="form-control" autoComplete="off" placeholder="Label" defaultValue={task.tag}>
                                        </input>
                                        <input className="form-control" name="date" type="date" defaultValue={task.date}>
                                        </input>
                                        <input type="submit" className="btn btn-primary update" value="Update">
                                        </input>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                );
            }
        }
        task = task[0];
        document.querySelector('#new-task').value = '';
        document.querySelector('#nothing').style.display = 'none';
        document.querySelector('#clearSchedule').style.animationPlayState = 'paused';
        document.querySelector('#clearSchedule').style.display = 'block';
        const checkID = `check${task.id}`;
        const accordionID = `accordion${task.id}`;
        const titleID = `title${task.id}`;
        const flushCollapse = `#flush-collapse${task.id}`;
        const flushCollapseID = `flush-collapse${task.id}`;
        const taskList = document.querySelector('#accordion');
        const newTask = document.createElement('div');
        const editorID = `editor${task.id}`;
        const formSubmit = `update/${task.id}`;
        const titleForm = `title-form${task.id}`
        newTask.id = `react${task.id}`
        taskList.append(newTask);

        ReactDOM.render(<Task title={task.title} tag={task.tag} />, document.getElementById(`react${task.id}`));
        document.getElementById(checkID).onchange = () => {
            checkOff(task.id);
        };

        document.getElementById(editorID).innerHTML = task.description;
        // create editor
        var quill = new Quill('#' + editorID, {
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

        // onChange handler
        document.getElementById(titleForm).onkeyup = () => {
            document.getElementById(titleID).innerText = document.getElementById(titleForm).value;
        }
        
        

    }
}
