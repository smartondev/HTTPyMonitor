import { ref } from 'vue'

export default function useExpand(expandedDefault: boolean = false) {
  const expandedRef = ref<boolean>(expandedDefault)
  const toggleExpanded = () => {
    expandedRef.value = !expandedRef.value
  }

  return {
    expandedState: expandedRef,
    toggleExpanded
  }
}