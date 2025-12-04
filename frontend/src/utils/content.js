// 页面内容
import homeContent from '../../content/pages/home.json'
import aboutContent from '../../content/pages/about.json'
import interestsContent from '../../content/pages/interests.json'
import contactContent from '../../content/pages/contact.json'
import blogContent from '../../content/pages/blog.json'
import loginContent from '../../content/pages/login.json'
import managementContent from '../../content/pages/management.json'
import singlePostContent from '../../content/pages/single-post.json'
import notFoundContent from '../../content/pages/not-found.json'

// 组件内容
import headerContent from '../../content/components/header.json'
import footerContent from '../../content/components/footer.json'

// 时间线单独导出
import timelineContent from '../../content/timeline.json'

// 统一导出
export const pages = {
  home: homeContent,
  about: aboutContent,
  interests: interestsContent,
  contact: contactContent,
  blog: blogContent,
  login: loginContent,
  management: managementContent,
  singlePost: singlePostContent,
  notFound: notFoundContent
}

export const components = {
  header: headerContent,
  footer: footerContent
}

export const timeline = timelineContent

// 便捷方法
export function getPageContent(pageName) {
  return pages[pageName] || {}
}

export function getComponentContent(componentName) {
  return components[componentName] || {}
}
