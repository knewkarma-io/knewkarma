A Reddit Data Analysis Toolkit
==============================

**Knew Karma** (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface** (**CLI**), and an **Application Programming Interface** (**API**) to enable easy integration in other Python projects and/or scripts.

.. image:: https://img.shields.io/pepy/dt/knewkarma?logo=pypi
   :target: https://pepy.tech/project/knewkarma/
   :alt: Pepy Total Downlods

.. image:: https://img.shields.io/pypi/v/knewkarma?logo=pypi
    :target: https://pypi.org/project/knewkarma
    :alt: PyPI Badge

.. image:: https://img.shields.io/snapcraft/v/knewkarma/latest/stable?logo=snapcraft&color=%23BB431A
    :target: https://snapcraft.io/knewkarma
    :alt: Snap Store Badge

.. image:: https://img.shields.io/opencollective/all/knewkarma?logo=open-collective
   :target: https://opencollective.com/knewkarma
   :alt: Open Collective backers and sponsors

.. image:: https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black
    :target: https://buymeacoffee.com/rly0nheart

.. list-table:: Knew Karma provides detailed access to Reddit data across various categories [see table below]:
   :widths: 25 25 50
   :header-rows: 1

   * - Category
     - Feature
     - Description
   * - **Post**
     - ``Data``
     - Retrieves an individual post's data.
   * -
     - ``Comments``
     - Retrieves an individual post's comments.
   * - **Posts**
     - ``New``
     - Retrieves new posts.
   * -
     - ``Reddit Front-Page``
     - Retrieves front-page posts.
   * -
     - ``Listing``
     - Retrieves posts from specified Reddit listings.
   * - **Search**
     - ``Users``
     - Searches for users.
   * -
     - ``Subreddits``
     - Searches for subreddits.
   * -
     - ``Posts``
     - Searches for posts.
   * - **Subreddit**
     - ``Profile``
     - Retrieves subreddit profile information.
   * -
     - ``Comments``
     - Retrieves comments from a subreddit.
   * -
     - ``Posts``
     - Retrieves posts from a subreddit.
   * -
     - ``Search Posts``
     - Returns a subreddit's posts that contain the specified keyword.
   * -
     - ``Wiki Pages``
     - Lists wiki pages in a subreddit.
   * -
     - ``Wiki Page``
     - Retrieves content from specific wiki pages.
   * - **Subreddits**
     - ``All``
     - Retrieves all subreddits.
   * -
     - ``Default``
     - Retrieves default subreddits.
   * -
     - ``New``
     - Retrieves new subreddits.
   * -
     - ``Popular``
     - Retrieves popular subreddits.
   * - **User**
     - ``Profile``
     - Retrieves user profile information.
   * -
     - ``Posts``
     - Retrieves user posts.
   * -
     - ``Comments``
     - Retrieves user comments.
   * -
     - ``Overview``
     - Retrieves user's most recent comment activity.
   * -
     - ``Search Posts``
     - Returns a user's posts that match with the specified search query.
   * -
     - ``Search Comments``
     - Returns a user's comments that match with the specified search query.
   * -
     - ``Top n Subreddits``
     - Identifies top subreddits based on user activity.
   * -
     - ``Moderated Subreddits``
     - Lists subreddits moderated by the user.
   * - **Users**
     - ``All``
     - Retrieves all users.
   * -
     - ``New``
     - Retrieves new users.
   * -
     - ``Popular``
     - Retrieves popular users.
