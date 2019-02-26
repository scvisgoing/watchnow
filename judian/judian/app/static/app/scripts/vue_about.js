var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue!',
        people: people,
        todos: [
            { text: 'Learn JavaScript' },
            { text: 'Learn Vue' },
            { text: 'Build something awesome' }
        ]
    },
    methods: {
        greet: function (name) {
            console.log('Hello from ' + name + '!')
        }
    }
});

app.todos.push({ text: 'Show me the money'})