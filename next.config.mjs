import nextra from 'nextra'

const withNextra = nextra({
  latex: false,
  defaultShowCopyCode: true,
  contentDirBasePath: '/posts'
})

export default withNextra({
  reactStrictMode: true
})
