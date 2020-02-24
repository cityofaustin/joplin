### Requirements
Last updated February 24, 2020

The only field required for save across all content types is Title
For publishing, only require English
Don't require any SEO or settings fields (except English slug, which is auto-generated for English)
Behavior when publishing from edit page: if not all the required fields are filled out, opens the edit page with the relevant error messaging

#### Service Page

- Required ✅
    - Description: 'short_description_en'
    - Steps : 'steps_en'
- Not Required ❌
    - Topic
    - Related Departments
    - Maps/app blocks
    - Additional content
    - contact
    - make top level
    
#### Info Page

- Required ✅
    - Description : 'description_en',
    - Content : 'additional_content_en',
- Not Required ❌
    - Topic
    - Related Departments
    - contact
    - make top level
    
#### Department Page

- Required ✅
    - What we do : 'what_we_do_en'
- Not Required ❌
    - Image
    - Mission
    - contact
    - Department Directors
    - job listing url
    - Top Services
    - Related Pages
    
#### Official document list
- Required ✅
    - Description : 'description_en'
    - Document entries : 'official_documents'
- Not Required ❌
    - Topic
    - Related departments

#### Guide
- Required ✅
    - Description : 'description_en'
    - Sections and Pages : 'sections'
    - Contact : contacts'
- Not Required ❌
    - Topic
    - Related departments
    - Image
    
#### Form container
- Required ✅
    - Description : 'description_en',
    - Formstack URL : 'form_url_en',
- Not Required ❌
    - Topic
    - Related departments
    
#### Topic
- Required ✅
    - Topic collection (Although this could be a weird chicken-egg situation. So maybe ❌) : 'topiccollections'
    - Top link: 'top_pages',
- Not Required ❌
    - Description (for now, but will want this later)
    - Image

#### Topic collection
- Required ✅
    - Theme : 'theme'
- Not Required ❌
    - Description (for now, but will want this later)
    - Image
    - Topic collection (topic collections can belong to parent topic collections)

#### Events

- Required ✅
    - Location physical address
    - Description
    - Event date *note: only start time should be required; end time is not required
    - Location of event

- Not Required ❌
    - The event is free
    - Fees
    - Registration
    - Related departments
    - Contact
    - Cancel

#### Location Pages

- Required ✅
    - Location physical address
- Not Required ❌
    - Banner image
    - Mailing address
    - Alternate name
    - Location contact info
    - Location details
    - Location hours
    - Related services
