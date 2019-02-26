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
        ]
    },
    methods: {
        greet: function (name) {
            console.log('Hello from ' + name + '!')
        },
        reverseMessage: function () {
            this.message = this.message.split('').reverse().join('')
        }
    },
    // lifecycle hooks give you the chance to add code at specific stages.
    // others like beforeCreate, beforeMount, mounted, beforeUpdate, updated, beforeDestroy, destroyed
    created: function () {
        // `this` points to the vm instance
        console.log('born at ' + this.timeToLoadPage)
    }
});

vm.todos.push({ text: 'Show me the money' })

// $watch is an instance method
vm.$watch('message', function (newValue, oldValue) {
    // This callback will be called when `vm.a` changes
    console.log('From ' + oldValue + ' to ' + newValue)
})

