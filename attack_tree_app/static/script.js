function createNode() {
    const label = document.getElementById('node-label').value;
    const value = document.getElementById('node-value').value;
    const parent_id = ...; // Some method to get the selected node's ID
    const type = ...; // Either 'sibling' or 'child' based on user input

    fetch('/create_node/', {
        method: 'POST',
        body: JSON.stringify({
            label: label,
            value: value,
            parent_id: parent_id,
            type: type
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update the tree visualization with the new node
        }
    });
}

function getTree() {
    fetch('/get_tree/')
    .then(response => response.json())
    .then(data => {
        // Update the tree visualization with the retrieved data
    });
}

function sumRoute() {
    const node_id = ...; // Some method to get the selected node's ID

    fetch('/sum_route/', {
        method: 'POST',
        body: JSON.stringify({
            node_id: node_id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        alert('Total value along the route: ' + data.sum);
    });
}

function exportTree() {
    fetch('/export_tree/')
    .then(response => response.blob())
    .then(blob => {
        const a = document.createElement('a');
        const url = URL.createObjectURL(blob);
        a.href = url;
        a.download = 'tree.json';
        a.click();
        URL.revokeObjectURL(url);
    });
}

function importTree() {
    const fileInput = document.getElementById('import-tree-file');
    const file = fileInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.readAsText(file, 'UTF-8');
        reader.onload = function(evt) {
            fetch('/import_tree/', {
                method: 'POST',
                body: evt.target.result,
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Refresh the tree visualization
                }
            });
        }
    }
}
