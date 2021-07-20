import axios from "axios"


const post = (async(url, data) => {
    try {
        const { data: result } = await axios.post(url, data)
        return result
    } catch (error) {
        return { msg: error.message }
    }
})

const get = (async(url, data = '') => {
    try {
        const { data: result } = await axios.get(url, data)
        return result
    } catch (error) {
        return { msg: error.message }
    }
})
const put = (async(url, data = '') => {
    try {
        const { data: result } = await axios.put(url, data)
        return result
    } catch (error) {
        return { msg: error.message }
    }
})
const _delete = (async(url, data = '') => {
    try {
        const { data: result } = await axios.delete(url, data)
        return result
    } catch (error) {
        return { msg: error.message }
    }
})

export { post, put, get, _delete }