//import _ from 'lodash' �o�y�u��b node.js �ϥ� https://stackoverflow.com/questions/47498395/lodash-or-any-import-causing-uncaught-syntaxerror-unexpected-token-import

// Define components that can compose in another component's template (like vue_about.html)
Vue.component('todo-item-simple', {
    template: '<li>This is a todo</li>',
})
// We want to pass data from parent scope into child components to let it can display real data.
// You will see v-bind:gc="item" that means we bind the data into this component's props gc.
// You also need to provide each component with a "key" using v-bind:key="item.id" but where is the componet's key? No see in props?
// We will learn later.
// Use component we separate app into two smaller units, the child is well-decoupled from the parent via the props interface.
// We can further improve out <grocery-item> component with more complex template and logic withou affecting the parent app.
Vue.component('grocery-item', {
    props: ['gc'],
    template: '<li>{{ gc.text }}</li>'
})
// In large app, divide whoe app into components to make development manageable. Here's an example of what an app's template might
// look like with components:
/**
 * <div id="app">
 *     <app-nav></app-nav>
 *     <app-view>
 *         <app-sidebar></app-sidebar>
 *         <app-content></app-content>
 *     </app-view>
 * </div>
 */

// the name vm(short for ViewModel) is a convention, although not strictly associated with the MVVM pattern.
// You can use vm.$data, Vue instance also proxies all the properties found on the data object, so vm.a = vm.$data.a
// But properites that start with _ or $ will not be proxied, You should use them explictly by vm.$data._a NOT vm._a
// When creating a Vue instance, pass it an options object, all Vue components are also Vue instances, and so accept the same options object
// (except for a few root-specific options)
// When vm is created, it adds all the properties found in its data object to Vue's reactivity system.
// data object properties �@�w�n�b��l���ɫ�N���w�A����ƫ�A�� vm.b = 'hi' �o���|Ĳ�o����view updates
// �b�ͦ� Vue ��Үɵ��� options ���i�ίS���覡���o�A��p vm.$el, vm.$data, ��ԲӪ��� vm.$el === document.getElementById('app')
// vm.$watch
var vm = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue!',
        timeToLoadPage: 'You loaded this page on ' + new Date().toLocaleString(),
        people: people,
        todos: [
            { text: 'Learn JavaScript' },
            { text: 'Learn Vue' },
            { text: 'Build something awesome' }
        ],
        groceryList: [
            { id: 0, text: 'Vegetables' },
            { id: 1, text: 'Cheese' },
            { id: 2, text: 'Whatever else humans are supposed to eat' }
        ],
        checkIt: true,
        //shitshit: 'ganlin baba',
        // �U���o��ӻ��� computed �ϥήɾ�(���ݥΨ���watcher)
        firstName: 'Foo',
        lastName: 'Bar',
        // �U���o��ӥΨӻ��� watcher �ϥήɾ�(��n���檺�F����������)
        question: '',
        answer: 'I cannot give you an answer until you ask a question!'
    },
    computed: {
        // a computed getter
        cpReverseMessage: function () {
            return this.message.split('').reverse().join('')
        },
        shitshit: function () {
            return 'ganlin gigi'
        },
        // �q�`�u�|�Ψ� computed �� getter �p�U
        //fullName: function () {
        //    return this.firstName + ' ' + this.lastName
        //}
        // ���]�i�H���� setter ���ݭn�ɡA�M��ϥ� vm.fullName = 'John Doe' �N�|�I�s�쥦�� setter �F
        fullName: {
            // getter
            get: function () {
                return this.firstName + ' ' + this.lastName
            },
            // setter
            set: function (newValue) {
                var names = newValue.split(' ')
                this.firstName = names[0]
                this.lastName = names[names.length - 1]
            }
        }
    },
    methods: {
        greet: function (name) {
            console.log('Hello from ' + name + '!')
        },
        reverseMessage: function () {
            this.message = this.message.split('').reverse().join('')
        },
        reverseMessage2: function () {
            return 'Good'
        },
        getAnswer: function () {
            if (this.question.indexOf('?') === -1) {
                this.answer = 'Questions usually contain a question mark. ;-)'
                return
            }
            this.answer = 'Thinking...'
            axios.get('https://yesno.wtf/api')
                .then(function (response) {
                    this.answer = _.capitalize(response.data.answer)
                })
                .catch(function (error) {
                    this.answer = 'Error! Could not reach the API. ' + error
                })
        }
    },
    watch: {
        // whenever question changes, this function will run
        question: function (newQuestion, oldQuestion) {
            this.answer = 'Waiting for you to stop typing...'
            this.getAnswer()//this.debouncedGetAnswer()
        }
    },
    // lifecycle hooks give you the chance to add code at specific stages.
    // others like beforeCreate, beforeMount, mounted, beforeUpdate, updated, beforeDestroy, destroyed
    created: function () {
        // `this` points to the vm instance
        console.log('born at ' + this.timeToLoadPage)
        // _.debounce is a function provided by lodash to limit how often a particularly expensive operation can be run.
        // In this case, we want to limit how often we access yesno.wtf/api, waiting until the user has completely
        // finished typing before making the ajax request.
        // To learn more about the _.debounce function (and its cousin _.throttle), visit: https://lodash.com/docs#debounce
        //this.debouncedGetAnswer = _.debounce(this.getAnswer, 500)
    }
});

vm.todos.push({ text: 'Show me the money' })

// $watch is an instance method
vm.$watch('message', function (newValue, oldValue) {
    // This callback will be called when `vm.a` changes
    console.log('From ' + oldValue + ' to ' + newValue)
})

// Template Syntax
// Vue compiles the templates into Virtual DOM render functions. If you are familiar with Virtual DOM, you can also directly write render functions instead
// of templates, with optional JSX support.
// Interpolations
// Text interpolation: �̰򥻪��j�w����, �ϥ� "Mustache" �y�k "{{ xxx }}" �򥻤W���|�Ѧ� text�A�Y�A�n���Ѧ� html �i�� v-html(���n�`�N)
// Mustache cannot be used inside HTML attributes. Instead, use a v-bind directive:
// <div v-bind:id="dynamicId"></div >
// <button v-bind:disabled="checkIt">Button</button> �Y checkIt �Ȭ� null/undefined/false ���i����
// {{ �̭��]�i��JavaScript Expressions }} �p {{ ok ? 'YES' : 'NO' }} �Ϊ� {{ message.split('').reverse().join('') }} �Ϊ� <div v-bind:id="'list-' + id"></div> // �̫�o�ӨҤl���F��
// �W���� Template expression �����ӽ������F�� {{ var a = 1 }} �o�O statement not an expression�A�t�~flow control�]���� {{ if(ok) {return message} }} �i��� ternary expressions
// <a v-bind:href="url"> ... </a> �o�O���� element �� href �ݩʸj�� url expression �᪺�ȡA�`�N url �|�Q��@ expression ��Ķ
// 2.6.0 �����h�F��dynamic argument�s�y�k <a v-bind:[attributename]="url"> ... </a> �o�䪺 attributename �|�ʺA����
// 2.6.0 �����h�F��dynamic argument�s�y�k <a v-on:[eventname]="doSomething"> ... </a> �Y eventname�Ȭ� focus ���N���� v-on:focus
// dynamic argument�n�`�N���O[ ] �̭����F��O�Q��@�r��B�z���A����]�t�ťթΤ޸��A�]���঳�j�g�A�u��U²��²�n
// Modifiers �i�D directive �n�ίS��覡�Ӹj�w�p .prevent modifier �i�D v-on ����Ĳ�oevent�ɭn�I�s event.preventDefault()
// <form v-on:submit.prevent="onSubmit"> ... </form>
// v-bind �� v-on �����Y�g�榡�A��p <a v-bind:href="url"> ... </a> �i������ v-bind ���� <a :href="url"> ... </a>
// <a v-on:click="doSomething"> ... </a> �i��� @ ���N�A�ܦ� <a @click="doSomething"> ... </a>

// Computed Properties & Watchers
// �e���ݹL in-template expression �u��²��A�g�o�ӽ����]���C�iŪ�ʡA���ɥi�Ҽ{ computed property�C
// ��vue�btemplate���ݨ� {{message}}�ɥ��|�յۥhdata object��A�Y�L�|�A�h computed ��
// �b console �� js ���n���Τ��n�� console.log(vm.reversedMessage) ������
// �Ʀܥi�H�� v-bind ���覡�Nelement���ݩʻP computed �j�b�@�_
// �� computed caching �� method ���t�O�Ӭݤ@�U
// <p> Method usage: [[ reverseMessage() ]]</p>
// <p> Computed usage: [[ cpReverseMessage ]]</p >
// computed vs watch
// �� a �ݭn�̾� b ���Ȩ��ܤƮɡA�i�� watch ����A���L���ɤ]�i�� computed �ѨM�A�ݺ����d��
// ���M computed properties �ܦn�Φ����M���ɫ�ݭn�a watch �F���A