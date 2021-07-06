import axios from "axios"


const post = (async (url,data)=>{
    try {
        const {data:result} = await axios.post(url,data)
        return result
    } catch (error) {
        return {msg:error.message}
    }
})

const get = (async (url,data='')=>{
    try {
        const {data:result} = await axios.get(url,data)
        return result
    } catch (error) {
        return {msg:error.message}
    }
})

export {post,get}