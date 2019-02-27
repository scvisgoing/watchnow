//import _ from 'lodash' 這句只能在 node.js 使用 https://stackoverflow.com/questions/47498395/lodash-or-any-import-causing-uncaught-syntaxerror-unexpected-token-import

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
// data object properties 一定要在初始的時後就給定，不能事後再用 vm.b = 'hi' 這不會觸發任何view updates
// 在生成 Vue 實例時給的 options 都可用特殊的方式取得，比如 vm.$el, vm.$data, 更詳細的說 vm.$el === document.getElementById('app')
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
        // 下面這兩個說明 computed 使用時機(不需用到兩個watcher)
        firstName: 'Foo',
        lastName: 'Bar',
        // 下面這兩個用來說明 watcher 使用時機(當要執行的東西比較複雜時)
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
        // 通常只會用到 computed 的 getter 如下
        //fullName: function () {
        //    return this.firstName + ' ' + this.lastName
        //}
        // 但也可以提供 setter 當有需要時，然後使用 vm.fullName = 'John Doe' 就會呼叫到它的 setter 了
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
// Text interpolation: 最基本的綁定型式, 使用 "Mustache" 語法 "{{ xxx }}" 基本上都會解成 text，若你要它解成 html 可用 v-html(但要注意)
// Mustache cannot be used inside HTML attributes. Instead, use a v-bind directive:
// <div v-bind:id="dynamicId"></div >
// <button v-bind:disabled="checkIt">Button</button> 若 checkIt 值為 null/undefined/false 都可接受
// {{ 裡面也可用JavaScript Expressions }} 如 {{ ok ? 'YES' : 'NO' }} 或者 {{ message.split('').reverse().join('') }} 或者 <div v-bind:id="'list-' + id"></div> // 最後這個例子很靈活
// 上面的 Template expression 不能放太複雜的東西 {{ var a = 1 }} 這是 statement not an expression，另外flow control也不行 {{ if(ok) {return message} }} 可改用 ternary expressions
// <a v-bind:href="url"> ... </a> 這是說把 element 的 href 屬性綁到 url expression 後的值，注意 url 會被當作 expression 解譯
// 2.6.0 版本多了個dynamic argument新語法 <a v-bind:[attributename]="url"> ... </a> 這邊的 attributename 會動態估值
// 2.6.0 版本多了個dynamic argument新語法 <a v-on:[eventname]="doSomething"> ... </a> 若 eventname值為 focus 那就等於 v-on:focus
// dynamic argument要注意的是[ ] 裡面的東西是被當作字串處理的，不能包含空白或引號，也不能有大寫，只能愈簡單簡好
// Modifiers 告訴 directive 要用特殊方式來綁定如 .prevent modifier 告訴 v-on 說當觸發event時要呼叫 event.preventDefault()
// <form v-on:submit.prevent="onSubmit"> ... </form>
// v-bind 跟 v-on 都有縮寫格式，比如 <a v-bind:href="url"> ... </a> 可直接把 v-bind 略掉 <a :href="url"> ... </a>
// <a v-on:click="doSomething"> ... </a> 可改用 @ 取代，變成 <a @click="doSomething"> ... </a>

// Computed Properties & Watchers
// 前面看過 in-template expression 只能簡潔，寫得太複雜也降低可讀性，此時可考慮 computed property。
// 當vue在template中看到 {{message}}時它會試著去data object找，若無會再去 computed 找
// 在 console 或 js 中要取用仍要用 console.log(vm.reversedMessage) 的型式
// 甚至可以用 v-bind 的方式將element的屬性與 computed 綁在一起
// 用 computed caching 跟 method 的差別來看一下
// <p> Method usage: [[ reverseMessage() ]]</p>
// <p> Computed usage: [[ cpReverseMessage ]]</p >
// computed vs watch
// 當 a 需要依據 b 的值來變化時，可用 watch 做到，不過此時也可用 computed 解決，看網頁範例
// 雖然 computed properties 很好用但仍然有時後需要靠 watch 達成，