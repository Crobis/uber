import { get_csrf_token } from './utils.js';
import EditorJS from '@editorjs/editorjs';
import Header from '@editorjs/header';
import ImageTool from '@editorjs/image';
import LinkTool from '@editorjs/link';
import Link from '@coolbytes/editorjs-link';

const editor = new EditorJS({
    holder: 'editorjs',
    tools: {
        header: {
            class: Header,
            inlineToolbar: true,
        },
        image: {
            class: ImageTool,
                config: {
                endpoints: {
                    byFile: 'http://localhost:8008/uploadFile', 
                    byUrl: 'http://localhost:8008/fetchUrl', 
                }
            }
        },
        linkTool: {
            class: LinkTool,
            config: {
              endpoint: '/service/get_url/',
              headers: {
                'X-CSRFToken': get_csrf_token(),
              }
            }
        },
        link: {
            class: Link,
            config: {
                shortcut: 'CMD+L',
                placeholder: "Enter URL",
                targets: ['_self', '_blank', '_parent', '_top'],
                defaultTarget: '_self',
                relations: ['', 'alternate', 'author', 'bookmark', 'canonical', 'external', 'help', 'license', 'manifest', 'me', 'next', 'nofollow', 'noopener', 'noreferrer', 'prev', 'search', 'tag'],
                defaultRelation: '',
                validate: false
            }
        }
    },
    onReady: () => {
        if(editor_data !== undefined){
            editor.render(editor_data);
        }
    },
});




document.getElementById('save-editorjs').addEventListener('click', async () => {
    try {
        const savedData = await editor.save(); 
        console.log('Editor data:', savedData); 
        

        const params = { 'action': 'save' }; 
        const payload = {
            ...savedData,
            ...params
        };

        let response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest', 
                'X-CSRFToken': get_csrf_token(), 
            },
            body: JSON.stringify(payload), 
        });

        const data = await response.json(); 
        if(data.redirect){
            window.location.replace(data.redirect);
        }
        editor.render(data);
        console.log('Loaded data:', data);

        console.log('Data saved successfully!');
    } catch (error) {
        console.error('Error saving data:', error);
    }
});


document.getElementById('load-editorjs').addEventListener('click', async () => {
    try {
        const params = { action: 'load' }; // Specify the action to load data

        // Fetch saved data from the server
        let response = await fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': get_csrf_token(),
            },
            body: JSON.stringify(params),
        });

        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        const data = await response.json(); // Parse JSON response
        console.log('Loaded data:', data);

        // Pass the loaded data to Editor.js
        editor.render(data); // Use render method to update editor content
        console.log('Editor data loaded successfully!');
    } catch (error) {
        console.error('Error loading data:', error);
    }
});


