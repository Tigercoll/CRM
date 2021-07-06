<template>
    <div>
        用户组件
    </div>
</template>

<script>
export default {
    methods:{
        test(){
            this.$axios.get('roles')
        }
    },
    mounted(){
        this.test()
    }

}
</script>