<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { randomInt } from '@/helpers/RandomHelper'

type Props = {
  wordsMin?: number
  wordsMax?: number
}

const props = withDefaults(defineProps<Props>(), {
  wordsMin: 30,
  wordsMax: 50
})

const placeholderList = ref<String[][]>([])
onMounted(() => {
  placeholderList.value = Array.from(
    { length: randomInt(props.wordsMin, props.wordsMax) },
    (_, __) => [`col-${randomInt(1, 3)}`, 'placeholder', `me-${randomInt(1, 6)}`]
  )
})
</script>

<template>
  <span v-for="(item, idx) in placeholderList" :key="idx" :class="item" />
</template>

<style scoped></style>